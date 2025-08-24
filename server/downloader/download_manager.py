from decimal import Context
from utils.parallel_runner import ParallelRunner
from downloader.task_downloader import TaskDownloader
import asyncio

class DownloadManager:
    def __init__(self, max_concurrent):
        self.runner = ParallelRunner(max_concurrent)
        self.pending_tasks = []
        self.downloaders = []

    async def stop(self):
        await self.runner.cancel()

    async def join(self):
        await self.runner.join()
    
    def get_status(self):
        return {
            "pending": self.pending_tasks,
            "running": [(downloader.download_task, downloader.human_readable_status()) for downloader in self.downloaders],
        }

    def submit(self, task):
        self.pending_tasks.append(task)
        self.runner.submit(self.process(task))

    async def process(self, task):
        self.pending_tasks.remove(task)
        downloader = TaskDownloader(task)
        self.downloaders.append(downloader)
        await downloader.run()
        self.downloaders.remove(downloader)

if __name__ == "__main__":
    from downloader.download_task import DownloadTask
    from context import Context
    async def test():
        async with Context(use_browser=True) as ctx:
            download_manager = DownloadManager(2)
            download_manager.submit(DownloadTask(sourceKey="girigirilove", url="https://anime.girigirilove.com/playGV26626-2-1/", dst="/tmp/1.mp4"))
            download_manager.submit(DownloadTask(sourceKey="girigirilove", url="https://anime.girigirilove.com/playGV26626-2-2/", dst="/tmp/2.mp4"))
            download_manager.submit(DownloadTask(sourceKey="girigirilove", url="https://anime.girigirilove.com/playGV26626-2-3/", dst="/tmp/3.mp4"))
            while True:
                print(download_manager.get_status())
                await asyncio.sleep(1)
                if len(download_manager.downloaders) == 0:
                    break
            await download_manager.join()
    asyncio.run(test())