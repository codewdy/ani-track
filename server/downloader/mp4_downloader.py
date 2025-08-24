from downloader.tmp_manager import TmpManager
from downloader.download_tracker import DownloadTracker
from downloader.simple_downloader import SimpleDownloader
from downloader.utils import run_cmd
import urllib
import re
import asyncio
import os

class MP4Downloader:
    def __init__(self, session, src, dst, tmp_dir):
        self.session = session
        self.src = src
        self.dst = dst
        self.tmp_dir = tmp_dir
        self.status = "preparing"

    async def run(self):
        async with TmpManager(self.tmp_dir) as tmp:
            output_file = tmp.allocate_file("output.mp4")
            self.download_tracker = DownloadTracker(1)
            self.status = "downloading"
            await SimpleDownloader(self.session, self.src, output_file, self.download_tracker).run()
            self.status = "copy result"
            await run_cmd("cp", output_file, self.dst + ".tmp")
            await run_cmd("mv", self.dst + ".tmp", self.dst)
            self.status = "done"


    def human_readable_status(self):
        if self.status == "downloading":
            return f"downloading: {self.download_tracker.human_readable_status()}"
        return self.status

if __name__ == "__main__":
    import asyncio
    import aiohttp
    from downloader.download_tracker import DownloadTracker
    async def test():
        async with aiohttp.ClientSession() as session:
            downloader = MP4Downloader(
                session, 
                "https://fe-video-qc.xhscdn.com/athena-creator/1040g0pg30u8okfv2l6d05pd6fqd214hmrc1ldco?filename=1.mp4", 
                "/tmp/oceans-3.mp4", 
                "/tmp/test")
            task = asyncio.create_task(downloader.run())
            while True:
                await asyncio.sleep(1)
                print(downloader.human_readable_status())
                if task.done():
                    break
            print(downloader.human_readable_status())
    asyncio.run(test())