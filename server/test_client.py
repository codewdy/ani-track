from aiohttp import ClientSession
import asyncio
from schema.api import AddAnimation, GetAnimations, GetAnimation, GetDownloadManagerStatus, SearchBangumi


async def request(session, url, req):
    async with session.post(url, data=req.model_dump_json()) as resp:
        return await resp.text()


async def test2():
    async with ClientSession() as session:
        req = GetAnimation.Request(animation_id=1)
        print(await request(session, "http://localhost:9876/api/get_animation", req))


asyncio.run(test2())
