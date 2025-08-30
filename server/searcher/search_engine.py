from searcher.searcher_list import searcher_list, searcher_dict
import asyncio
import aiohttp


class SearchFunctor:
    def __init__(self, keyword):
        self.keyword = keyword

    async def __call__(self, searcher):
        try:
            return await searcher.search(self.keyword)

        except Exception as e:
            return [
                {
                    "error": str(e),
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

        return sum(results, [])

    async def search_episode(self, source_key, url, channel_name):
        return await self.searcher_dict[source_key].search_episode(url, channel_name)


if __name__ == "__main__":
    from context import Context

    search_engine = SearchEngine()

    async def run():
        async with Context() as ctx:
            return await search_engine.search("碧蓝之海")
    print(asyncio.run(run()))
