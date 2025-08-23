class SimpleDownloader:
    def __init__(self, session, src, dst, download_tracker = None):
        self.session = session
        self.src = src
        self.dst = dst
        self.download_tracker = download_tracker

    async def run(self):
        async with self.session.get(self.src) as resp:
            resp.raise_for_status()
            if self.download_tracker is not None:
                self.download_tracker.add_slice(resp.content_length)
            with open(self.dst, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    if self.download_tracker is not None:
                        self.download_tracker.add_bytes_downloaded(len(chunk))

if __name__ == "__main__":
    import asyncio
    import aiohttp
    from downloader.download_tracker import DownloadTracker
    async def test():
        async with aiohttp.ClientSession() as session:
            download_tracker = DownloadTracker(1)
            downloader = SimpleDownloader(session, "https://fe-video-qc.xhscdn.com/athena-creator/1040g0pg30u8okfv2l6d05pd6fqd214hmrc1ldco?filename=1.mp4", "/tmp/oceans.mp4", download_tracker)
            task = asyncio.create_task(downloader.run())
            while True:
                await asyncio.sleep(1)
                print(download_tracker.human_readable())
                if task.done():
                    break
            print(download_tracker.human_readable())
    asyncio.run(test())