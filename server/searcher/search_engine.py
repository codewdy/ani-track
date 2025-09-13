from searcher.searcher_list import searcher_list, searcher_dict
import asyncio
import aiohttp
import traceback


class SearchFunctor:
    def __init__(self, keyword):
        self.keyword = keyword

    async def __call__(self, searcher):
        try:
            return await asyncio.wait_for(searcher.search(self.keyword), timeout=5), []

        except Exception as e:
            return [], [
                {
                    "error": traceback.format_exc(),
                    "name": searcher.name,
                    "icon": searcher.icon,
                }
            ]


class SearchEngine:
    def __init__(self):
        self.searcher_list = searcher_list()
        self.searcher_dict = searcher_dict()

    async def search(self, keyword):
        results = await asyncio.gather(
            *map(
                SearchFunctor(keyword),
                self.searcher_list,
            )
        )

        return sum([res[0] for res in results], []), sum([res[1] for res in results], [])

    async def search_episode(self, source_key, url, channel_name):
        return await self.searcher_dict[source_key].search_episode(url, channel_name)


if __name__ == "__main__":
    from context import Context
    import json

    search_engine = SearchEngine()

    async def run():
        async with Context() as ctx:
            return await search_engine.search("碧蓝之海")
    print(asyncio.run(run()))
    open("result.json", "w").write(json.dumps(
        asyncio.run(run()), ensure_ascii=False))
