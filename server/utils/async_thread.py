import asyncio


class AsyncThread:
    def __init__(self):
        self._thread = None
        self._loop = None
        self._event = None

    def start(self):
        self._thread = threading.Thread(
            target=lambda: asyncio.run(self.main_loop()))
        self._thread.start()

    async def main_loop(self):
        await self.init()
        self._loop = asyncio.get_running_loop()
        self._event.set()
        await self.loop()

    async def init(self):
        pass

    async def loop(self):
        pass

    @staticmethod
    def task(func):
        def wrapper(self, *args, **kwargs):
            self._event.wait()
            self._loop.call_soon_threadsafe(
                lambda: func(self, *args, **kwargs))
        return wrapper
