import sys

import settings
from core.logger import setup_loggers


def run_app():
    import uvloop
    from aiohttp import web
    from app import create_app

    uvloop.install()
    application = create_app()
    web.run_app(
        application,
        host=settings.APP_HOST,
        port=settings.APP_PORT
    )


if __name__ == "__main__":
    setup_loggers(settings.LOG_LEVEL, settings.THIRD_PARTY_LOG_LEVEL)
    eval(sys.argv[1].split()[0])()
