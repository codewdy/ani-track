from searcher.web_searcher.subject_searcher import SubjectSearcher
from searcher.web_searcher.channel_searcher import ChannelSearcher
from searcher.web_searcher.resource_searcher import ResourceSearcher
import asyncio


class Searcher:
    def __init__(self, config):
        self.key = config["key"]
        self.name = config["name"]
        self.icon = config["iconUrl"]
        self.subject_searcher = SubjectSearcher(config["searchConfig"])
        self.channel_searcher = ChannelSearcher(config["searchConfig"])
        self.resource_searcher = ResourceSearcher(config["searchConfig"])

    async def search(self, keyword):
        result = await self.subject_searcher.search(keyword)
        result = result[:5]
        channel_result = await asyncio.gather(
            *map(
                self.channel_searcher.search,
                [i["link"] for i in result],
            )
        )

        for subject, channel in zip(result, channel_result):
            subject["channel"] = channel
            subject["source"] = self.name
            subject["sourceKey"] = self.key
            subject["icon"] = self.icon
        return result

    async def search_episode(self, url, name):
        channels = await self.channel_searcher.search(url)
        for channel in channels:
            if channel["name"] == name:
                return channel
        raise Exception("Channel not found.")

    async def search_resource(self, url):
        return await self.resource_searcher.search(url)


if __name__ == "__main__":
    import json
    import asyncio
    from pathlib import Path
    from context import Context

    with open(Path(__file__).parent / "searcher.json", "r") as f:
        config = json.load(f)
    searcher = Searcher(config["searchers"][0])

    async def run():
        async with Context() as ctx:
            return await searcher.search("碧蓝之海")

    print(asyncio.run(run()))
