from schema.config import Config
from schema.db import Animation, Channel, AnimationStatus, DownloadStatus
from schema.api import *
from tracker.db_manager import DBManager
import asyncio
import os
from context import Context
from tracker.updater import Updater
from tracker.path_manager import PathManager
from bangumi import bangumi
from utils.simple_service import SimpleService
from searcher.search_engine import SearchEngine
from utils.filename_allocate import allocate_filename


class Tracker(SimpleService):
    def __init__(self, config: Config):
        self.config = config
        self.path_manager = PathManager(self.config)
        self.search_engine = SearchEngine()

    async def start(self):
        self.context = Context(
            use_browser=True, tmp_dir=self.config.download.tmp_dir)
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

    @SimpleService.api
    async def add_animation(self, request: AddAnimation.Request) -> AddAnimation.Response:
        db = self.db_manager.db
        animation_id = db.next_animation_id
        channel_id = 1
        db.next_animation_id = db.next_animation_id + 1

        resource_dir = self.config.resource.default
        ani_dirname = allocate_filename(
            request.name, [x.dirname for x in db.animations.values()])
        channel_dir = allocate_filename(request.channel_name, [])
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
        self.db_manager.save(force=True)
        return AddAnimation.Response(animation_id=animation_id)

    @SimpleService.api
    async def get_animations(self, request: GetAnimations.Request) -> GetAnimations.Response:
        db = self.db_manager.db
        is_new = request.version != self.db_manager.version
        if not is_new:
            return GetAnimations.Response(is_new=False, version=self.db_manager.version, animations=[])
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
        return GetAnimations.Response(is_new=True, version=self.db_manager.version, animations=animations)

    @SimpleService.api
    async def get_download_manager_status(self, request: GetDownloadManagerStatus.Request) -> GetDownloadManagerStatus.Response:
        status = self.updater.download_manager.get_status()
        return GetDownloadManagerStatus.Response(
            downloading=[
                GetDownloadManagerStatus.DownloadTask(
                    resource_name=task.meta["resource_name"],
                    status=s,
                )
                for task, s in status["running"]
            ],
            pending=[
                GetDownloadManagerStatus.DownloadTask(
                    resource_name=task.meta["resource_name"],
                    status="Pending",
                )
                for task in status["pending"]
            ],
        )

    @SimpleService.api
    async def search_bangumi(self, request: SearchBangumi.Request) -> SearchBangumi.Response:
        search_result = await bangumi.search(request.keyword)
        return SearchBangumi.Response(animations=[
            SearchBangumi.AnimationInfo(
                id=item["id"],
                name=item["name"],
                image=item["image"],
            )
            for item in search_result
        ])

    @SimpleService.api
    async def search_channel(self, request: SearchChannel.Request) -> SearchChannel.Response:
        search_result, search_error = await self.search_engine.search(request.keyword)
        response = SearchChannel.Response(channels=[], search_errors=[])
        for source_search_result in search_result:
            for item in source_search_result["channel"]:
                response.channels.append(SearchChannel.ChannelInfo(
                    name=f"{source_search_result['name']} - {item['name']} - {source_search_result['source']}",
                    search_name=item["name"],
                    url=source_search_result["link"],
                    source_key=source_search_result["sourceKey"],
                    episodes=[
                        SearchChannel.EpisodeInfo(
                            name=ep["episode"],
                            url=ep["episode_link"],
                        )
                        for ep in item["episodes"]
                    ],
                ))
        for error in search_error:
            response.search_errors.append(SearchChannel.SearchErrorInfo(
                source=error["name"],
                error=error["error"],
            ))
        return response

    @SimpleService.api
    async def set_watch_status(self, request: SetWatchStatus.Request) -> SetWatchStatus.Response:
        db = self.db_manager.db
        db.animations[request.animation_id].status = request.status
        self.db_manager.mark_dirty()
        return SetWatchStatus.Response()

    @SimpleService.api
    async def get_animation_info(self, request: GetAnimationInfo.Request) -> GetAnimationInfo.Response:
        db = self.db_manager.db
        animation = db.animations[request.animation_id]
        episodes = []
        for ep_index, ep in enumerate(animation.channels[animation.current_channel].episodes):
            episodes.append(GetAnimationInfo.EpisodeInfo(
                name=ep.name,
                url=str(self.path_manager.episode_web_path(
                    db, animation.animation_id, animation.current_channel, ep_index)),
            ))
        return GetAnimationInfo.Response(
            animation_id=animation.animation_id,
            name=animation.name,
            bangumi_id=animation.bangumi_id,
            icon_url=animation.icon_url,
            status=animation.status,
            watched_episode=animation.watched_episode,
            watched_episode_time=animation.watched_episode_time,
            episodes=episodes,
        )

    @SimpleService.api
    async def set_watched_time(self, request: SetWatchedTime.Request) -> SetWatchedTime.Response:
        db = self.db_manager.db
        animation = db.animations[request.animation_id]
        animation.watched_episode = request.watched_episode
        animation.watched_episode_time = request.watched_episode_time
        self.db_manager.mark_dirty()
        return SetWatchedTime.Response()


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
                print(await tracker.get_download_manager_status(GetDownloadManagerStatus.Request()))
                await asyncio.sleep(10)

    async def test2():
        tracker = Tracker(config)
        async with tracker:
            req = GetAnimations.Request(version="")
            return await tracker.get_animations(req)

    async def test3():
        tracker = Tracker(config)
        async with tracker:
            req = SearchBangumi.Request(keyword="测试")
            print(await tracker.search_bangumi(req))

    async def test4():
        tracker = Tracker(config)
        async with tracker:
            req = SearchChannel.Request(keyword="碧蓝之海")
            return await tracker.search_channel(req)

    async def test5():
        tracker = Tracker(config)
        async with tracker:
            req = GetAnimationInfo.Request(animation_id=1)
            return await tracker.get_animation_info(req)

    open("result.json", "w").write(
        asyncio.run(test5()).model_dump_json(indent=2))
