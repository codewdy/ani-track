import asyncio
from schema.config import Config
from tracker.download_manager import DownloadManager


class Updater:
    def __init__(self, config: Config, db_manager: DBManager):
        self.config = config
        self.db_manager = db_manager
        self.download_manager = DownloadManager(
            self.config.tracker.max_download_concurrent)
        self.search_engine = SearchEngine()

    def update(self, animation_id, channel_id):
        with self.db_manager.db() as db:
            channel = db.animations[animation_id].channels[channel_id].model_copy(
                deep=True)
        episode = self.search_engine.search_episode(
            channel.sourceKey, channel.link, channel.search_name)
        if len(episode["episodes"]) > len(channel.episodes):
            with self.db_manager.db() as db:
                for i in range(len(channel.episodes), len(episode["episodes"])):
                    mutable_channel = db.animations[animation_id].channels[channel_id]
                    mutable_channel.episodes.append(Episode(
                        name=episode["episodes"][i]["name"],
                        url=episode["episodes"][i]["url"],
                        filename="",
                        download_status=DownloadStatus.Running,
                    ))
