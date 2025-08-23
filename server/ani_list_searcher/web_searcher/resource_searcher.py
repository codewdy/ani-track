from urllib.parse import urlparse, parse_qs

_PREFIX = [".mp4", ".m3u8"]

class RequestResourceHandler:
    def __init__(self):
        self.result = None
    
    async def handle_request(self, route):
        self.result = route.request.url
        await route.abort()

    @staticmethod
    async def get(browser, url):
        result = RequestResourceHandler()
        page = await browser.new_page()
        await page.route("**/*.{mp4,m3u8}", result.handle_request)
        await page.goto(url, timeout=60000)
        await page.title()
        await page.close()
        return result.result

class ResourceParser:
    def __init__(self):
        pass

    def parse(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if "url" in query_params:
            return query_params["url"][0]
        return url

class ResourceSearcher:
    def __init__(self, searchConfig):
        self.parser = ResourceParser()

    async def search(self, browser, url):
        rst = await RequestResourceHandler.get(browser, url)
        return self.parser.parse(rst)

if __name__ == "__main__":
    import asyncio
    from playwright.async_api import async_playwright
    searcher = ResourceSearcher(None)
    async def test():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            print(await searcher.search(browser, "https://anime.girigirilove.com/playGV26626-1-1/"))
            print(await searcher.search(browser, "https://vdm10.com/play/13842-2-1.html"))
            print(await searcher.search(browser, "https://www.fqdm.cc/index.php/vod/play/id/11579/sid/2/nid/1.html"))
            print(await searcher.search(browser, "https://www.yinghua2.com/index.php/vod/play/id/56591/sid/4/nid/1.html"))
            print(await searcher.search(browser, "https://zgacgn.com/play/19246-2-0.html"))
            print(await searcher.search(browser, "https://dm1.xfdm.pro/watch/124/1/1.html"))
            print(await searcher.search(browser, "https://omofun.icu/vod/play/id/136511/sid/4/nid/1.html"))
            print(await searcher.search(browser, "https://www.mxdmp.com/play/2193/1/1/"))
            await browser.close()
    asyncio.run(test())