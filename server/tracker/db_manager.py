from schema.db import AnimationDB
from utils.atomic_file_write import atomic_file_write
import os
import asyncio
import uuid


class DBManager:
    def __init__(self, config):
        self.config = config
        self.db = None
        self._save_task = None
        self._dirty = False
        self.version = self.uuid()

    async def start(self):
        if os.path.exists(self.config.tracker.db_file):
            self.db = AnimationDB.parse_file(self.config.tracker.db_file)
        else:
            self.db = AnimationDB()
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
        try:
            await self._save_task
        except BaseException:
            pass
        self.save()

    def uuid(self):
        return str(uuid.uuid4())

    def dump_db(self):
        return self.db.model_dump_json(indent=2)

    async def save_loop(self):
        while True:
            await asyncio.sleep(self.config.tracker.save_interval.total_seconds())
            self.save()

    def mark_dirty(self):
        self.version = self.uuid()
        self._dirty = True

    def save(self, force=False):
        if self._dirty or force:
            self._dirty = False
            db_dump = self.dump_db()
            atomic_file_write(self.config.tracker.db_file, db_dump)
