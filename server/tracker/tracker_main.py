from schema.config import Config
from schema.db import Animation, Channel, AnimationStatus
from schema.api import AddAnimation
from tracker.db_manager import DBManager
import asyncio
import os
from context import Context
from tracker.updater import Updater


class Tracker:
    def __init__(self, config: Config):
        self.config = config

    async def start(self):
        self.context = Context(
            use_browser=True, tmp_dir=self.config.tracker.tmp_dir)
        await self.context.__aenter__()
        self.db_manager = DBManager(self.config)
        self.updater = Updater(self.config, self.db_manager)
        await self.db_manager.start()
        await self.updater.start()

    async def stop(self):
        await self.updater.stop()
        await self.db_manager.stop()
        await self.context.__aexit__(None, None, None)

    async def __aenter__(self):
        await self.start()

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()

    async def add_animation(self, request: AddAnimation.Request) -> AddAnimation.Response:
        db = self.db_manager.db
        animation_id = db.next_animation_id
        channel_id = 1
        db.next_animation_id = db.next_animation_id + 1

        resource_dir = self.config.resource.default
        ani_dirname = str(animation_id)
        channel_dir = str(channel_id)
        os.makedirs(self.config.resource.dirs[resource_dir] +
                    "/" + ani_dirname + "/" + channel_dir, exist_ok=True)

        animation = Animation(
            animation_id=animation_id,
            name=request.name,
            bangumi_id=request.bangumi_id,
            icon_url=request.icon_url,
            resource_dir=resource_dir,
            dirname=ani_dirname,
            status=request.status,
            channels={
                channel_id: Channel(
                    name=request.channel_name,
                    search_name=request.channel_search_name,
                    url=request.channel_url,
                    source_key=request.channel_source_key,
                    dirname=channel_dir,
                    tracking=True,
                    latest_update=0,
                    episodes=[],
                )
            },
            next_channel_id=2,
            current_channel=channel_id,
        )
        db.animations[animation_id] = animation
        await self.updater.update(animation_id, channel_id)
        return AddAnimation.Response(animation_id=animation_id)


if __name__ == "__main__":
    config = Config.model_validate_json(open("config.json").read())

    async def test():
        try:
            os.remove("ani_track.db")
        except:
            pass
        tracker = Tracker(config)
        async with tracker:
            req = AddAnimation.Request(
                name="测试",
                bangumi_id="123",
                icon_url="https://www.baidu.com",
                status=AnimationStatus.Wanted,
                channel_name="测试",
                channel_search_name="简中",
                channel_url="https://anime.girigirilove.com/GV26626/",
                channel_source_key="girigirilove",
            )
            await tracker.add_animation(req)
            await asyncio.sleep(200)
    asyncio.run(test())
