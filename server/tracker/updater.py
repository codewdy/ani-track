import asyncio
from turtle import down
from schema.config import Config
from downloader.download_manager import DownloadManager
from tracker.db_manager import DBManager
from searcher.search_engine import SearchEngine
from schema.db import Episode, DownloadStatus
from datetime import datetime
from downloader.download_task import DownloadTask
from tracker.path_manager import PathManager, PathType
from functools import partial


class Updater:
    def __init__(self, config: Config, db_manager: DBManager):
        self.config = config
        self.db_manager = db_manager
        self.download_manager = DownloadManager(
            self.config.tracker.max_download_concurrent)
        self.search_engine = SearchEngine()
        self.path_manager = PathManager(self.config, PathType.LocalPath)

    async def start(self):
        pass

    async def stop(self):
        await self.download_manager.stop()

    async def update_loop(self):
        pass

    def download_done(self, animation_id, channel_id, episode_id):
        print(f"download done {animation_id} {channel_id} {episode_id}")
        with self.db_manager.db() as db:
            db.animations[animation_id].channels[channel_id].episodes[episode_id].download_status = DownloadStatus.Finished

    def download_failed(self, animation_id, channel_id, episode_id, error):
        with self.db_manager.db() as db:
            db.animations[animation_id].channels[channel_id].episodes[episode_id].download_status = DownloadStatus.Failed
            db.animations[animation_id].channels[channel_id].episodes[episode_id].download_error = str(
                error)

    async def update(self, animation_id, channel_id):
        with self.db_manager.db() as db:
            channel = db.animations[animation_id].channels[channel_id].model_copy(
                deep=True)
        episode = await self.search_engine.search_episode(
            channel.source_key, channel.url, channel.search_name)
        download_task = []
        with self.db_manager.db() as db:
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
                    on_finished=partial(self.download_done,
                                        animation_id, channel_id, i),
                    on_error=partial(self.download_failed,
                                     animation_id, channel_id, i),
                ))
            mutable_channel.latest_update = datetime.now()
        for task in download_task:
            self.download_manager.submit(task)
