import argparse

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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Endpoint для запуска приложения PositiveBucks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--api", action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    setup_loggers(settings.LOG_LEVEL, settings.THIRD_PARTY_LOG_LEVEL)
    args = parse_args()
    run_app() if args.api else print("Do nothing")
