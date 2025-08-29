from schema.config import Config
from schema.db import AnimationDB
from utils.lock_guard import LockGuard


class DBManager:
    def __init__(self, config):
        self.config = config
        self._db = None
        self._save_task = None

    async def start(self):
        if os.path.exists(self.config.db_file):
            self._db = LockGuard(AnimationDB.parse_file(self.config.db_file))
        else:
            self._db = LockGuard(AnimationDB())
        self._save_task = asyncio.create_task(self.save_loop())

    async def stop(self):
        if self._save_task is not None:
            self._save_task.cancel()
            await self._save_task
        self.save()

    def db(self):
        return self._db

    def save(self):
        with open(self.config.db_file, "w") as f:
            with self.db() as db:
                f.write(db.model_dump_json(indent=2))

    async def save_loop(self):
        while True:
            await asyncio.sleep(self.config.tracker.save_interval.total_seconds())
            self.save()
