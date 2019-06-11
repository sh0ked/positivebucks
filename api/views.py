from aiohttp import web

from core.utils import json_to_str

HTTP_OK = 200
HTTP_CREATED = 201


def _form_response(data: (dict, list), status_code: int = HTTP_OK) -> web.Response:
    if isinstance(data, dict) or isinstance(data, list):
        content_type = "application/json"
        body = json_to_str(data).encode("utf-8")
    else:
        raise Exception(f"Unexpected '{type(data).__name__}' data type for response")

    return web.Response(
        body=body,
        content_type=content_type,
        status=status_code
    )


async def create_user(request: web.Request):
    return _form_response({})


async def get_user(request: web.Request):
    return _form_response({})


async def list_users(request: web.Request):
    return _form_response({})


async def create_order(request: web.Request):
    return _form_response({})


async def get_order(request: web.Request):
    return _form_response({})


async def list_orders(request: web.Request):
    return _form_response({})


async def complete_orders(request: web.Request):
    return _form_response({})


async def active_orders(request: web.Request):
    return _form_response({})


async def waiting_orders(request: web.Request):
    return _form_response({})


ROUTES = [
    web.post("/users", create_user),
    web.get("/users/{uid:\d+}", get_user),
    web.get("/users", list_users),
    web.post("/orders", create_order),
    web.get("/orders/{uid:\d+}", get_order),
    web.get("/orders", list_orders),
    web.get("/orders/complete", complete_orders),
    web.get("/orders/active", active_orders),
    web.get("/orders/waiting", waiting_orders),
]
