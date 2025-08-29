from schema.config import Config
from schema.db import AnimationDB
from schema.api import AddAnimation
from server.tracker.db_manager import DBManager


class Tracker:
    def __init__(self, config: Config):
        self.config = config

    async def init(self):
        self.db_manager = DBManager(self.config)
        await self.db_manager.start()

    async def add_animation(self, request: AddAnimation.Request) -> AddAnimation.Response:
        pass
