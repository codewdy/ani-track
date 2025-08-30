import asyncio
import threading
import traceback


class AsyncThread:
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._futures = set()
        self._running = False

    async def start(self):
        self._thread = threading.Thread(target=self._loop.run_forever)
        self._thread.start()
        self._running = True

    async def stop(self):
        self._running = False
        futures = self._futures.copy()
        for future in futures:
            await future
        self._loop.call_soon_threadsafe(self._loop.stop)
        await asyncio.to_thread(self._thread.join)

    async def abort(self):
        self._running = False
        self._loop.call_soon_threadsafe(self._loop.stop)
        await asyncio.to_thread(self._thread.join)

    def done(self, future):
        self._futures.remove(future)

    async def protected(self, coro):
        try:
            return await coro
        except Exception as e:
            traceback.print_exc()
            return e

    @staticmethod
    def threadrun(func):
        def wrap(self, *args, **kwargs):
            if not self._running:
                raise RuntimeError("AsyncThread not running")
            future = asyncio.run_coroutine_threadsafe(
                self.protected(func(self, *args, **kwargs)), self._loop)
            rst = asyncio.wrap_future(future)
            self._futures.add(rst)
            rst.add_done_callback(self.done)
            return rst
        return wrap


if __name__ == "__main__":
    class TestAsyncThread(AsyncThread):
        @AsyncThread.threadrun
        async def test_task(self):
            print("test_task start")
            await asyncio.sleep(1)
            print("test_task end")

    async def test():
        async_thread = TestAsyncThread()
        await async_thread.start()
        async_thread.test_task()
        await async_thread.stop()
    asyncio.run(test())
