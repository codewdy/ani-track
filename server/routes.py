from aiohttp import web
from ani_list_searcher.search_engine import SearchEngine

routes = web.RouteTableDef()
ani_search_engine = SearchEngine(["https://sub.creamycake.org/v1/css1.json"])


@routes.get("/ani_search/{name}")
async def ani_search(request):
    return web.json_response(await ani_search_engine.search(request.match_info["name"]))


@routes.get("/")
async def hello(request):
    return web.Response(text="Hello, world")
