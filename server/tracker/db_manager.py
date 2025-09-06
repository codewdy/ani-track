from schema.db import AnimationDB
from utils.atomic_file_write import atomic_file_write
import os
import asyncio


class DBManager:
    def __init__(self, config):
        self.config = config
        self.db = None
        self._save_task = None

    async def start(self):
        if os.path.exists(self.config.tracker.db_file):
            self.db = AnimationDB.parse_file(self.config.tracker.db_file)
            self._last_db_dump = self.dump_db()
        else:
            self.db = AnimationDB()
            self._last_db_dump = ""
            self.save(force=True)
        self._save_task = asyncio.create_task(self.save_loop())

    async def stop(self):
        if self._save_task is not None:
            self._save_task.cancel()
            try:
                await self._save_task
            except BaseException:
                pass
        self._save_task.cancel()
        self.save()

    def dump_db(self):
        return self.db.model_dump_json(indent=2)

    async def save_loop(self):
        while True:
            await asyncio.sleep(self.config.tracker.save_interval.total_seconds())
            self.save()

    def save(self, force=False):
        db_dump = self.dump_db()
        if db_dump != self._last_db_dump or force:
            atomic_file_write(self.config.tracker.db_file, db_dump)
            self._last_db_dump = db_dump
