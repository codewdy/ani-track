from ani_list_searcher.searcher_list import searcher_dict
from downloader.mp4_downloader import MP4Downloader
from downloader.m3u8_downloader import M3U8Downloader

class TaskDownloader:
    def __init__(self, session, browser, download_task, tmp_dir):
        self.download_task = download_task
        self.browser = browser
        self.session = session
        self.tmp_dir = tmp_dir
        self.status = "preparing"
    
    def get_downloader(self, video_url):
        if video_url.endswith(".mp4"):
            return MP4Downloader(self.session, video_url, self.download_task.dst, self.tmp_dir)
        elif video_url.endswith(".m3u8"):
            return M3U8Downloader(self.session, video_url, self.download_task.dst, self.tmp_dir)
        raise ValueError(f"Unknown task type: {self.download_task.type}")

    async def run(self):
        self.status = "searching task"
        searcher = searcher_dict()[self.download_task.sourceKey]
        video_url = await searcher.search_resource(self.browser, self.download_task.url)
        self.downloader = self.get_downloader(video_url)
        self.status = "downloading"
        await self.downloader.run()
        self.status = "done"
    
    def human_readable_status(self):
        if self.status == "downloading":
            return self.downloader.human_readable_status()
        return self.status

if __name__ == "__main__":
    import asyncio
    import aiohttp
    from downloader.download_task import DownloadTask
    from playwright.async_api import async_playwright

    download_task = DownloadTask(
        sourceKey = "girigirilove",
        url = "https://anime.girigirilove.com/playGV26626-1-1/",
        dst = "/tmp/oceans-4.mp4",
    )
    
    async def run():
        async with aiohttp.ClientSession() as session:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                downloader = TaskDownloader(session, browser, download_task, "/tmp/test")
                task = asyncio.create_task(downloader.run())
                while True:
                    await asyncio.sleep(1)
                    print(downloader.human_readable_status())
                    if task.done():
                        break
                print(downloader.human_readable_status())    
                await browser.close()

    asyncio.run(run())
