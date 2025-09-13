from aiohttp import web
from tracker.tracker_main import Tracker
from schema.config import Config
import sys

config = Config.model_validate_json(open(sys.argv[-1]).read())
tracker = Tracker(config)


async def on_startup(app):
    await tracker.start()


async def on_cleanup(app):
    await tracker.stop()


async def make_app():
    app = web.Application()
    app.add_routes(tracker.create_routes())
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == "__main__":
    web.run_app(make_app(), port=config.service.api_port)
