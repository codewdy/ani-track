from schema.config import Config
from schema.db import AnimationDB
from schema.api import AddAnimation
from server.tracker.db_manager import DBManager


class BackgroudTracker(AsyncThread):
    def __init__(self, config: Config):
        self.config = config

    async def start(self):
        await super().start()
        await self.init()

    async def stop(self):
        await self.db_manager.stop()
        await super().stop()

    @AsyncThread.threadrun
    async def init(self):
        self.db_manager = DBManager(self.config)
        await self.db_manager.start()

    def db(self):
        return self.db_manager.db()
