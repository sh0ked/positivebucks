from aiohttp import web


class ApiApplication(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def create_app():
    from api import middlewares
    from api.views import ROUTES as API_ROUTES

    api_app = ApiApplication(
        middlewares=[
            middlewares.request_middleware
        ],
    )
    api_app.router.add_routes(API_ROUTES)

    return api_app
