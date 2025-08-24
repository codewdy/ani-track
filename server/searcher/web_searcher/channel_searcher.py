from utils.beautiful import request, to_text
import urllib


class IndexGroupedParser:
    def __init__(
        self,
        selectChannelNames,
        selectEpisodeLists,
        selectEpisodesFromList,
        selectEpisodeLinksFromList,
        **kwargs,
    ):
        self.selectChannelNames = selectChannelNames
        self.selectEpisodeLists = selectEpisodeLists
        self.selectEpisodesFromList = selectEpisodesFromList
        self.selectEpisodeLinksFromList = selectEpisodeLinksFromList

    def parse_episode_list(self, src, list):
        episodes_tag = [i for i in list.select(self.selectEpisodesFromList)]
        if self.selectEpisodeLinksFromList:
            episode_links = [
                i["href"]
                for i in list.select(self.selectEpisodeLinksFromList)
                if i.has_attr("href") and i["href"] != ""
            ]
        else:
            episode_links = []
        result = []
        for i in range(len(episodes_tag)):
            href = episode_links[i] if i < len(episode_links) else episodes_tag[i]["href"]
            if href == "" or href.startswith("javascript:"):
                continue
            result.append(
                {
                    "episode": to_text(episodes_tag[i]),
                    "episode_link": urllib.parse.urljoin(src, href),
                }
            )

        if len(result) == 0:
            raise FileNotFoundError(f"No Episode Result")
        return result

    def parse(self, src, soup):
        channel_names = [to_text(i) for i in soup.select(self.selectChannelNames)]
        episode_lists = [
            self.parse_episode_list(src, i)
            for i in soup.select(self.selectEpisodeLists)
        ]
        return [
            {"name": name, "episodes": list}
            for name, list in zip(channel_names, episode_lists)
        ]


class UnknownParser:
    def __init__(self, type):
        self.type = type

    def parse(self, src, soup):
        raise ValueError(f"Unknown channel parser: {self.type}")


class ChannelSearcher:
    def __init__(self, searchConfig):
        if searchConfig["channelFormatId"] == "index-grouped":
            self.parser = IndexGroupedParser(
                **searchConfig["selectorChannelFormatFlattened"]
            )
        else:
            self.parser = UnknownParser(searchConfig["channelFormatId"])

    async def search(self, url):
        soup = await request(url)
        result = self.parser.parse(url, soup)
        return result


if __name__ == "__main__":
    import json
    import asyncio
    from pathlib import Path
    from context import Context

    with open(Path(__file__).parent / "searcher.json", "r") as f:
        config = json.load(f)
    searcher = ChannelSearcher(config["searchers"][0]["searchConfig"])

    async def run():
        async with Context() as ctx:
            return await searcher.search(
                "https://anime.girigirilove.com/GV26626/"
            )

    print(asyncio.run(run()))
