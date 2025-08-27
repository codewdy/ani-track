import asyncio
import threading


class AsyncThread:
    def __init__(self):
        self._thread = None
        self._loop = None
        self._event = None

    def start(self):
        self._event = threading.Event()
        self._thread = threading.Thread(target=self.thread_main)
        self._thread.start()
        self._event.wait()

    def thread_main(self):
        asyncio.run(self.main_loop())
        self._loop.run_forever()

    async def main_loop(self):
        await self.init()
        self._loop = asyncio.get_running_loop()
        self._event.set()

    async def init(self):
        pass

    @staticmethod
    def task(func):
        def wrapper(self, *args, **kwargs):
            self._loop.call_soon_threadsafe(
                lambda: func(self, *args, **kwargs))
        return wrapper
