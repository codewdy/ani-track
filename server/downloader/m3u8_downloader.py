from downloader.tmp_manager import TmpManager
from downloader.download_tracker import DownloadTracker
from downloader.simple_downloader import SimpleDownloader
from downloader.utils import run_cmd
import urllib
import re
import asyncio
import os

class M3U8Downloader:
    def __init__(self, session, src, dst, tmp_dir):
        self.session = session
        self.src = src
        self.dst = dst
        self.tmp_dir = tmp_dir
        self.status = "preparing"

    def select_sub_list(self, lines):
        r = re.compile(r"RESOLUTION=([0-9]+)x([0-9]+)")
        x, y = 0, 0
        rst = (-1, "")
        for line in lines:
            if line.startswith("#"):
                m = r.search(line)
                if m:
                    x, y = int(m.group(1)), int(m.group(2))
                continue
            if x * y > rst[0]:
                rst = (x * y, line)
        if rst[0] == -1:
            raise ValueError("No valid sub list found")
        return rst[1]

    async def download_meta(self, file):
        await SimpleDownloader(self.session, self.src, file).run()
        with open(file, "r") as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        master_playlist = False
        for line in lines:
            if line.startswith("#"):
                continue
            if line.endswith(".m3u8"):
                master_playlist = True
                break
        if master_playlist:
            self.src = urllib.parse.urljoin(self.src, self.select_sub_list(lines))
            await self.download_meta()
        else:
            return [urllib.parse.urljoin(self.src, line) for line in lines if (not line.startswith("#")) and line != ""]

    async def ffmpeg(self, src_m3u8, fragments, dst):
        with open(src_m3u8, "r") as f:
            lines = f.readlines()
            current_fragment = 0
            newlines = []
            for line in lines:
                if line.startswith("#"):
                    newlines.append(line)
                else:
                    newlines.append(fragments[current_fragment] + "\n")
                    current_fragment += 1
            print(newlines)
        with open(src_m3u8, "w") as f:
            f.writelines(newlines)
        await run_cmd(
            "ffmpeg", "-y", "-allowed_extensions", "ALL", "-i", src_m3u8, "-acodec", "copy", "-vcodec", "copy",
             "-bsf:a", "aac_adtstoasc", dst)

    async def run(self):
        async with TmpManager(self.tmp_dir) as tmp:
            self.status = "downloading m3u8 meta"
            src_m3u8_file = tmp.allocate_file("src.m3u8")
            urls = await self.download_meta(src_m3u8_file)
            self.download_tracker = DownloadTracker(len(urls))
            self.status = "downloading"
            fragments = []
            for i, url in enumerate(urls):
                fn = tmp.allocate_file(f"fragment_{i}.ts")
                fragments.append(fn)
                await SimpleDownloader(self.session, url, fn, self.download_tracker).run()
            self.status = "running ffmpeg"
            output_file = tmp.allocate_file("output.mp4")
            await self.ffmpeg(src_m3u8_file, fragments, output_file)
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
            downloader = M3U8Downloader(
                session, 
                "https://m3u8.girigirilove.com/zijian/oldanime/2025/07/cht/GrandBlueS2CHT/01/playlist.m3u8", 
                "/tmp/oceans-2.mp4", 
                "/tmp/test")
            task = asyncio.create_task(downloader.run())
            while True:
                await asyncio.sleep(1)
                print(downloader.human_readable_status())
                if task.done():
                    break
            print(downloader.human_readable_status())
    asyncio.run(test())