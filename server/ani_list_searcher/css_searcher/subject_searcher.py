from ani_list_searcher.css_searcher.utils import request, to_text
import urllib


class IndexedParser:
    def __init__(self, selectNames, selectLinks, **kwargs):
        self.selectNames = selectNames
        self.selectLinks = selectLinks

    def parse(self, src, soup):
        text = [to_text(i) for i in soup.select(self.selectNames)]
        href = [
            i["href"]
            for i in soup.select(self.selectLinks)
            if i.has_attr("href") and i["href"] != ""
        ]

        if len(text) != len(href):
            raise RuntimeError(
                f"cannot parse search result len(text)={len(text)} len(href)={len(href)}"
            )
        if len(text) == 0:
            raise FileNotFoundError(f"No Search Result")

        return [
            {"name": name, "link": urllib.parse.urljoin(src, href)}
            for name, href in zip(text, href)
        ]


class AParser:
    def __init__(self, selectLists, **kwargs):
        self.selectLists = selectLists

    def parse(self, src, soup):
        tokens = soup.select(self.selectLists)

        if len(tokens) == 0:
            raise FileNotFoundError(f"No Search Result")

        return [
            {"name": to_text(token), "link": urllib.parse.urljoin(src, token["href"])}
            for token in tokens
        ]


class UnknownParser:
    def __init__(self, type):
        self.type = type

    def parse(self, src, soup):
        raise ValueError(f"Unknown subject parser: {self.type}")


class SubjectSearcher:
    def __init__(self, searchConfig):
        self.searchUrl = searchConfig["searchUrl"]
        if searchConfig["subjectFormatId"] == "indexed":
            self.parser = IndexedParser(**searchConfig["selectorSubjectFormatIndexed"])
        elif searchConfig["subjectFormatId"] == "a":
            self.parser = AParser(**searchConfig["selectorSubjectFormatA"])
        else:
            self.parser = UnknownParser(searchConfig["subjectFormatId"])

    def request_url(self, query):
        return self.searchUrl.format(keyword=urllib.parse.quote(query))

    async def search(self, session, query):
        request_url = self.request_url(query)
        soup = await request(session, request_url)
        return self.parser.parse(request_url, soup)


if __name__ == "__main__":
    import requests
    import json
    import asyncio
    import aiohttp

    config = json.loads(requests.get("https://sub.creamycake.org/v1/css1.json").text)
    searcher = SubjectSearcher(
        config["exportedMediaSourceDataList"]["mediaSources"][0]["arguments"][
            "searchConfig"
        ]
    )

    async def run():
        async with aiohttp.ClientSession() as session:
            return await searcher.search(session, "碧蓝之海")

    print(asyncio.run(run()))
