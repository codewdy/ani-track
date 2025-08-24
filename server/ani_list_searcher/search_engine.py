from ani_list_searcher.searcher_list import searcher_list
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

    async def search(self, keyword):
        results = await asyncio.gather(
            *map(
                SearchFunctor(keyword),
                self.searcher_list,
            )
        )
            
        return sum(results, [])


if __name__ == "__main__":
    from context import Context

    search_engine = SearchEngine()
    async def run():
        async with Context() as ctx:
            return await search_engine.search("碧蓝之海")
    print(asyncio.run(run()))
