from ani_list_searcher.searcher_list import SearcherList
import asyncio
import aiohttp


class SearchFunctor:
    def __init__(self, session, keyword):
        self.session = session
        self.keyword = keyword

    async def __call__(self, searcher):
        try:
            return await searcher.search(self.session, self.keyword)

        except Exception as e:
            return [
                {
                    "error": str(e),
                    "name": searcher.name,
                    "icon": searcher.icon,
                }
            ]


class SearchEngine:
    def __init__(self, sources):
        self.searcher_list = SearcherList(sources, 60 * 60 * 24)

    async def search(self, keyword):
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=3)
        ) as session:
            results = await asyncio.gather(
                *map(
                    SearchFunctor(session, keyword),
                    await self.searcher_list.searchers(session),
                )
            )

        return sum(results, [])


if __name__ == "__main__":
    search_engine = SearchEngine(["https://sub.creamycake.org/v1/css1.json"])
    print(asyncio.run(search_engine.search("碧蓝之海")))
