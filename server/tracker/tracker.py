from schema.config import Config
from schema.db import AnimationDB
from schema.api import AddAnimation
from server.tracker.db_manager import DBManager


class Tracker:
    def __init__(self, config: Config):
        self.config = config
        self.background_tracker = BackgroudTracker(self.config)

    async def start(self):
        await self.background_tracker.start()

    async def stop(self):
        await self.background_tracker.stop()

    async def add_animation(self, request: AddAnimation.Request) -> AddAnimation.Response:
        pass
