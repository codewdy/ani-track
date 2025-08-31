from aiohttp import web
from tracker.tracker_main import Tracker
from schema.config import Config


async def make_app():
    config = Config.model_validate_json(open("config.json").read())
    tracker = Tracker(config)
    await tracker.start()
    app = web.Application()
    app.add_routes(tracker.create_routes())
    return app


if __name__ == "__main__":
    web.run_app(make_app(), port=8080)
