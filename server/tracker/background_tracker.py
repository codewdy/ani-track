from schema.config import Config
from tracker.db_manager import DBManager
from tracker.updater import Updater
from utils.async_thread import AsyncThread
from context import Context


class BackgroudTracker(AsyncThread):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config

    async def start(self):
        await super().start()
        await self.init()

    async def stop(self):
        await self.stop_task()
        await super().stop()

    @AsyncThread.threadrun
    async def init(self):
        self.db_manager = DBManager(self.config)
        self.updater = Updater(self.config, self.db_manager)
        self.context = Context(
            use_browser=True, tmp_dir=self.config.tracker.tmp_dir)
        await self.context.__aenter__()
        await self.db_manager.start()
        await self.updater.start()

    @AsyncThread.threadrun
    async def stop_task(self):
        await self.updater.stop()
        await self.db_manager.stop()
        await self.context.__aexit__(None, None, None)

    @AsyncThread.threadrun
    async def update_channel(self, animation_id, channel_id):
        await self.updater.update(animation_id, channel_id)

    def db(self):
        return self.db_manager.db()
