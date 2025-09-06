from aiohttp import ClientSession
import asyncio
from schema.api import AddAnimation, GetAnimations, GetAnimation, GetDownloadManagerStatus, SearchBangumi


async def request(session, url, req):
    async with session.post(url, data=req.model_dump_json()) as resp:
        return await resp.text()


async def test2():
    async with ClientSession() as session:
        while True:
            req = GetDownloadManagerStatus.Request()
            print(await request(session, "http://localhost:5373/api/get_download_manager_status", req))
            await asyncio.sleep(1)


asyncio.run(test2())
