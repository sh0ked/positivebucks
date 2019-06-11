import logging
from aiohttp import web

from api.app import create_app as create_api_app


log = logging.getLogger(__name__)


class BaseApplication(web.Application):
    def __init__(self):
        super().__init__()
        self.on_startup.append(self.startup_func)
        self.on_cleanup.append(self.cleanup_func)
        self.on_shutdown.append(self.shutdown_func)

    async def startup_func(self, app):
        log.info("Starting app...")

    async def cleanup_func(self, app):
        log.info("Cleanup in progress...")

    async def shutdown_func(self, app):
        log.info("Shutting down...")


async def healthcheck(request):
    return web.Response(status=200, text="OK", content_type="text/plain")


def create_app():
    base_app = BaseApplication()
    base_app.add_routes([
        web.get("/healthcheck", healthcheck),
    ])

    api_app = create_api_app()
    base_app.add_subapp("/api/v1/", api_app)

    return base_app
