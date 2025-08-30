import asyncio
from schema.config import Config
from downloader.download_manager import DownloadManager
from tracker.db_manager import DBManager
from searcher.search_engine import SearchEngine
from schema.db import Episode, DownloadStatus
from datetime import datetime


class Updater:
    def __init__(self, config: Config, db_manager: DBManager):
        self.config = config
        self.db_manager = db_manager
        self.download_manager = DownloadManager(
            self.config.tracker.max_download_concurrent)
        self.search_engine = SearchEngine()

    async def start(self):
        pass

    async def stop(self):
        pass

    async def update(self, animation_id, channel_id):
        with self.db_manager.db() as db:
            channel = db.animations[animation_id].channels[channel_id].model_copy(
                deep=True)
        episode = await self.search_engine.search_episode(
            channel.source_key, channel.url, channel.search_name)
        with self.db_manager.db() as db:
            mutable_channel = db.animations[animation_id].channels[channel_id]
            for i in range(len(channel.episodes), len(episode["episodes"])):
                mutable_channel.episodes.append(Episode(
                    name=episode["episodes"][i]["episode"],
                    url=episode["episodes"][i]["episode_link"],
                    filename="",
                    download_status=DownloadStatus.Running,
                ))
            mutable_channel.latest_update = datetime.now()
