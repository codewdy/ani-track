from ani_list_searcher.css_searcher.searcher import Searcher as CssSearcher
import json
import time
import traceback


class SearcherList:
    def __init__(self, sources, timeout):
        self.sources = sources
        self.timeout = timeout
        self.cache = None
        self.last_update_time = None

    def searcher(self, config):
        if config["factoryId"] == "web-selector":
            return CssSearcher(config["arguments"])
        else:
            raise ValueError(f"unknown factoryId={config['factoryId']}")

    async def searchers_uncached(self, session):
        rst = []
        for src in self.sources:
            async with session.get(src) as resp:
                if resp.status != 200:
                    raise ValueError(f"get searcher list error: status={resp.status}")
                config = json.loads(await resp.text())
            rst.extend(
                [
                    self.searcher(searcher_config)
                    for searcher_config in config["exportedMediaSourceDataList"][
                        "mediaSources"
                    ]
                ]
            )
        return rst

    async def searchers(self, session):
        if self.cache is None or (time.time() - self.last_update_time) > self.timeout:
            self.last_update_time = time.time()
            try:
                self.cache = await self.searchers_uncached(session)
            except Exception as e:
                print(f"Create Cache Error: {traceback.format_exc()}")
        return self.cache


if __name__ == "__main__":
    import asyncio
    import aiohttp

    searcher_list = SearcherList(
        ["https://sub.creamycake.org/v1/css1.json"], 60 * 60 * 24
    )

    async def run():
        async with aiohttp.ClientSession() as session:
            return await searcher_list.searchers(session)

    print(asyncio.run(run()))
