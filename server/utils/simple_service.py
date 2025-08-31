from aiohttp import web


class SimpleService:
    @staticmethod
    def api(func):
        func.__api__ = True
        return func

    @staticmethod
    def _wrap(func):
        request_type = func.__annotations__["request"]

        async def wrapper(request):
            text = await request.text()
            request = request_type.model_validate_json(text)
            return web.json_response(text=(await func(request)).model_dump_json())
        return wrapper

    def create_routes(self):
        routes = web.RouteTableDef()
        for name, func in self.__class__.__dict__.items():
            if hasattr(func, "__api__"):
                routes.post(
                    f"/api/{name}")(SimpleService._wrap(getattr(self, name)))
        return routes
