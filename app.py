import logging
from aiohttp import web

from api.app import create_app as create_api_app


log = logging.getLogger(__name__)


async def healthcheck(request):
    """Простая проверка "живо ли" приложение

    :param request:
    :return:
    """
    return web.Response(status=200, text="OK", content_type="text/plain")


def _setup_docs(app):
    """Интеграция Swagger в приложение

    :param app:
    :return:
    """
    from os import path

    import jinja2
    import aiohttp_jinja2

    @aiohttp_jinja2.template("index.html")
    async def swagger_home(request):
        return {}

    async def openapi_document(request):
        return web.FileResponse(openapi_document_file)

    docs_path = path.abspath(path.join(path.dirname(__file__), "docs"))
    templates_path = path.join(docs_path, "templates")
    static_path = path.join(docs_path, "static")
    openapi_document_file = path.join(docs_path, "openapi.yaml")

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(templates_path))
    app.router.add_route("GET", "/docs", swagger_home)
    app.router.add_route("GET", "/docs/openapi.yaml", openapi_document)
    app.router.add_static("/docs/static", static_path)
    app['static_root_url'] = "/docs/static"


def create_app():
    """Создание базового приложения

    :return:
    """
    base_app = web.Application()
    base_app.add_routes([
        web.get("/healthcheck", healthcheck),
    ])

    api_app = create_api_app()
    base_app.add_subapp("/api/v1/", api_app)

    _setup_docs(base_app)
    return base_app
