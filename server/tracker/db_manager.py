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
        if os.path.exists(self.config.db_file):
            self.db = AnimationDB.parse_file(self.config.db_file)
        else:
            self.db = AnimationDB()
        self._save_task = asyncio.create_task(self.save_loop())

    async def stop(self):
        if self._save_task is not None:
            self._save_task.cancel()
            try:
                await self._save_task
            except BaseException:
                pass
        self.save()

    def save(self):
        dbjson = self.db.model_dump_json(indent=2)
        atomic_file_write(self.config.db_file, dbjson)

    async def save_loop(self):
        while True:
            await asyncio.sleep(self.config.tracker.save_interval.total_seconds())
            self.save()
