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


class Updater:
    def __init__(self, config: Config, db_manager: DBManager):
        self.config = config
        self.db_manager = db_manager
        self.download_manager = DownloadManager(
            self.config.tracker.max_download_concurrent)
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
            channel = animation.channels[channel_id]
            if channel.tracking and datetime.now().astimezone() - channel.latest_update > self.config.tracker.update_interval:
                await self.update(animation.animation_id, channel_id)

    def download_done(self, animation_id, channel_id, episode_id):
        db = self.db_manager.db
        db.animations[animation_id].channels[channel_id].episodes[episode_id].download_status = DownloadStatus.Finished

    def download_failed(self, animation_id, channel_id, episode_id, error):
        db = self.db_manager.db
        db.animations[animation_id].channels[channel_id].episodes[episode_id].download_status = DownloadStatus.Failed
        db.animations[animation_id].channels[channel_id].episodes[episode_id].download_error = str(
            error)

    async def download_all(self):
        db = self.db_manager.db
        for animation in db.animations.values():
            channel_id = animation.current_channel
            channel = animation.channels[channel_id]
            for idx, episode in enumerate(channel.episodes):
                if episode.download_status == DownloadStatus.Running:
                    self.download_manager.submit(DownloadTask(
                        sourceKey=channel.source_key,
                        url=episode.url,
                        dst=str(self.path_manager.episode_path(
                            db, animation.animation_id, channel_id, idx)),
                        meta={
                            "resource_name": self.path_manager.resource_name(db, animation.animation_id, channel_id, idx),
                        },
                        on_finished=partial(self.download_done,
                                            animation.animation_id, channel_id, idx),
                        on_error=partial(self.download_failed,
                                         animation.animation_id, channel_id, idx),
                    ))

    async def update(self, animation_id, channel_id):
        db = self.db_manager.db
        channel = db.animations[animation_id].channels[channel_id].model_copy(
            deep=True)
        episode = await self.search_engine.search_episode(
            channel.source_key, channel.url, channel.search_name)
        download_task = []
        db = self.db_manager.db
        mutable_animation = db.animations[animation_id]
        mutable_channel = mutable_animation.channels[channel_id]
        for i in range(len(mutable_channel.episodes), len(episode["episodes"])):
            mutable_channel.episodes.append(Episode(
                name=episode["episodes"][i]["episode"],
                url=episode["episodes"][i]["episode_link"],
                filename=f"{i+1}.mp4",
                download_status=DownloadStatus.Running,
            ))
            download_task.append(DownloadTask(
                sourceKey=mutable_channel.source_key,
                url=episode["episodes"][i]["episode_link"],
                dst=str(self.path_manager.episode_path(
                    db, animation_id, channel_id, i)),
                meta={
                    "resource_name": self.path_manager.resource_name(db, animation_id, channel_id, i),
                },
                on_finished=partial(self.download_done,
                                    animation_id, channel_id, i),
                on_error=partial(self.download_failed,
                                 animation_id, channel_id, i),
            ))
            mutable_channel.latest_real_update = datetime.now()
        mutable_channel.latest_update = datetime.now()
        if mutable_channel.latest_update - mutable_channel.latest_real_update > self.config.tracker.untrack_timeout:
            mutable_channel.tracking = False
        for task in download_task:
            self.download_manager.submit(task)
