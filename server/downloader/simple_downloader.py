class SimpleDownloader:
    def __init__(self, session, src, dst, download_speed_tracker):
        self.session = session
        self.src = src
        self.dst = dst
        self.download_speed_tracker = download_speed_tracker

    async def run(self):
        async with self.session.get(self.src) as resp:
            with open(self.dst, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    self.download_speed_tracker.add_bytes_downloaded(len(chunk))

if __name__ == "__main__":
    import asyncio
    import aiohttp
    from downloader.download_speed_tracker import DownloadSpeedTracker
    async def test():
        async with aiohttp.ClientSession() as session:
            download_speed_tracker = DownloadSpeedTracker()
            downloader = SimpleDownloader(session, "https://sub.creamycake.org/v1/css1.json", "test.json", download_speed_tracker)
            await downloader.run()
            print(download_speed_tracker.get_human_readable_speed())
    asyncio.run(test())