import asyncio
import enum
from turtle import down, update
from schema.config import Config
from downloader.download_manager import DownloadManager
from tracker.db_manager import DBManager
from searcher.search_engine import SearchEngine
from schema.db import Episode, DownloadStatus
from datetime import datetime
from downloader.download_task import DownloadTask
from tracker.path_manager import PathManager
from functools import partial
from utils.filename_allocate import allocate_filename


class Updater:
    def __init__(self, config: Config, db_manager: DBManager):
        self.config = config
        self.db_manager = db_manager
        self.download_manager = DownloadManager(
            self.config.download.concurrent)
        self.search_engine = SearchEngine()
        self.path_manager = PathManager(self.config)

    async def start(self):
        self.task = asyncio.create_task(self.update_loop())
        await self.download_all()

    async def stop(self):
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass
        await self.download_manager.stop()

    async def update_loop(self):
        while True:
            await self.update_all()
            await asyncio.sleep(self.config.tracker.update_interval.total_seconds())

    async def update_all(self):
        db = self.db_manager.db
        for animation in db.animations.values():
            channel_id = animation.current_channel
            await self.update(animation.animation_id, channel_id)

    def download_done(self, animation_id, channel_id, episode_id):
        db = self.db_manager.db
        print("Dowload done: ", self.path_manager.resource_name(
            db, animation_id, channel_id, episode_id))
        db.animations[animation_id].channels[channel_id].episodes[episode_id].download_status = DownloadStatus.Finished
        self.db_manager.mark_dirty()

    def download_failed(self, animation_id, channel_id, episode_id, error):
        db = self.db_manager.db
        print("Dowload failed: ", self.path_manager.resource_name(
            db, animation_id, channel_id, episode_id), error)
        db.animations[animation_id].channels[channel_id].episodes[episode_id].download_status = DownloadStatus.Failed
        db.animations[animation_id].channels[channel_id].episodes[episode_id].download_error = error
        self.db_manager.mark_dirty()

    def submit_download(self, animation_id, channel_id, episode_id):
        db = self.db_manager.db
        episode = db.animations[animation_id].channels[channel_id].episodes[episode_id]
        print("Dowloading: ", self.path_manager.resource_name(
            db, animation_id, channel_id, episode_id))
        self.download_manager.submit(DownloadTask(
            sourceKey=db.animations[animation_id].channels[channel_id].source_key,
            url=episode.url,
            dst=str(self.path_manager.episode_path(
                db, animation_id, channel_id, episode_id)),
            meta={
                "resource_name": self.path_manager.resource_name(db, animation_id, channel_id, episode_id),
            },
            on_finished=partial(self.download_done,
                                animation_id, channel_id, episode_id),
            on_error=partial(self.download_failed,
                             animation_id, channel_id, episode_id),
            retry=self.config.download.retry,
            retry_interval=self.config.download.retry_interval.total_seconds(),
            timeout=self.config.download.timeout.total_seconds(),
        ))

    async def download_all(self):
        db = self.db_manager.db
        for animation in db.animations.values():
            channel_id = animation.current_channel
            channel = animation.channels[channel_id]
            for idx, episode in enumerate(channel.episodes):
                if episode.download_status == DownloadStatus.Running:
                    self.submit_download(
                        animation.animation_id, channel_id, idx)

    async def update(self, animation_id, channel_id):
        db = self.db_manager.db
        channel = db.animations[animation_id].channels[channel_id].model_copy(
            deep=True)
        episode = await self.search_engine.search_episode(
            channel.source_key, channel.url, channel.search_name)
        update_episodes = []
        db = self.db_manager.db
        mutable_animation = db.animations[animation_id]
        mutable_channel = mutable_animation.channels[channel_id]
        for i in range(len(mutable_channel.episodes), len(episode["episodes"])):
            mutable_channel.episodes.append(Episode(
                name=episode["episodes"][i]["episode"],
                url=episode["episodes"][i]["episode_link"],
                filename=allocate_filename(
                    f"{episode["episodes"][i]["episode"]}.mp4", [x.filename for x in mutable_channel.episodes]),
                download_status=DownloadStatus.Running,
            ))
            update_episodes.append(i)
            mutable_channel.latest_update = datetime.now().astimezone()
            self.db_manager.mark_dirty()
        if datetime.now().astimezone() - mutable_channel.latest_update > self.config.tracker.untrack_timeout:
            mutable_channel.tracking = False
            self.db_manager.mark_dirty()
        for i in update_episodes:
            self.submit_download(animation_id, channel_id, i)
