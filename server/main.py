from routes import routes
from aiohttp import web

app = web.Application()
app.add_routes(routes)
web.run_app(app)
