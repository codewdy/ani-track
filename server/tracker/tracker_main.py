from schema.config import Config
from schema.db import Animation, Channel, AnimationStatus, DownloadStatus
from schema.api import AddAnimation, GetAnimations, GetAnimation
from tracker.db_manager import DBManager
import asyncio
import os
from context import Context
from tracker.updater import Updater
from tracker.path_manager import PathManager


class Tracker:
    def __init__(self, config: Config):
        self.config = config
        self.path_manager = PathManager(self.config)

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

    async def get_animations(self, request: GetAnimations.Request) -> GetAnimations.Response:
        db = self.db_manager.db
        animations = []
        for animation in db.animations.values():
            total_episode = 0
            for ep in animation.channels[animation.current_channel].episodes:
                if ep.download_status == DownloadStatus.Finished:
                    total_episode += 1
                else:
                    break
            animations.append(GetAnimations.AnimationInfo(
                animation_id=animation.animation_id,
                name=animation.name,
                bangumi_id=animation.bangumi_id,
                icon_url=animation.icon_url,
                status=animation.status,
                watched_episode=animation.watched_episode +
                (1 if animation.watched_episode_time_percent >
                 self.config.tracker.episode_watch_end_ratio else 0),
                total_episode=total_episode,
            ))
        return GetAnimations.Response(animations=animations)

    async def get_animation(self, request: GetAnimation.Request) -> GetAnimation.Response:
        db = self.db_manager.db
        animation = db.animations[request.animation_id]
        episodes = []
        for ep_index, ep in enumerate(animation.channels[animation.current_channel].episodes):
            episodes.append(GetAnimation.EpisodeInfo(
                name=ep.name,
                url=str(self.path_manager.episode_web_path(
                    db, animation.animation_id, animation.current_channel, ep_index)),
            ))
        return GetAnimation.Response(animation=GetAnimation.AnimationInfo(
            animation_id=animation.animation_id,
            name=animation.name,
            bangumi_id=animation.bangumi_id,
            icon_url=animation.icon_url,
            status=animation.status,
            watched_episode=animation.watched_episode,
            watched_episode_time=animation.watched_episode_time,
            episodes=episodes,
        ))


if __name__ == "__main__":
    config = Config.model_validate_json(open("config.json").read())

    async def test1():
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
            for i in range(100):
                print(await tracker.get_animations(GetAnimations.Request()))
                await asyncio.sleep(10)

    async def test2():
        tracker = Tracker(config)
        async with tracker:
            req = GetAnimation.Request(animation_id=1)
            print(await tracker.get_animation(req))
    asyncio.run(test2())
