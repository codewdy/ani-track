from ani_list_searcher.web_searcher.subject_searcher import SubjectSearcher
from ani_list_searcher.web_searcher.channel_searcher import ChannelSearcher
from ani_list_searcher.web_searcher.resource_searcher import ResourceSearcher
import asyncio


class Searcher:
    def __init__(self, config):
        self.name = config["name"]
        self.icon = config["iconUrl"]
        self.subject_searcher = SubjectSearcher(config["searchConfig"])
        self.channel_searcher = ChannelSearcher(config["searchConfig"])
        self.resource_searcher = ResourceSearcher(config["searchConfig"])

    async def search(self, session, keyword):
        result = await self.subject_searcher.search(session, keyword)
        result = result[:5]
        channel_result = await asyncio.gather(
            *map(
                self.channel_searcher.search,
                [session] * len(result),
                [i["link"] for i in result],
            )
        )

        for subject, channel in zip(result, channel_result):
            subject["channel"] = channel
            subject["source"] = self.name
            subject["icon"] = self.icon
        return result
    
    async def search_resource(self, session, url):
        return await self.resource_searcher.search(session, url)


if __name__ == "__main__":
    import requests
    import json
    import asyncio
    import aiohttp

    config = json.loads(requests.get("https://sub.creamycake.org/v1/css1.json").text)
    searcher = Searcher(
        config["exportedMediaSourceDataList"]["mediaSources"][0]["arguments"]
    )

    async def run():
        async with aiohttp.ClientSession() as session:
            return await searcher.search(session, "碧蓝之海")

    print(asyncio.run(run()))
