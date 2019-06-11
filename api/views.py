from aiohttp import web


async def create_user(request: web.Request):
    return web.Response(
        body="create user",
        content_type="text/plain",
        status=200
    )


async def get_user(request: web.Request):
    return web.Response(
        body="get user by id",
        content_type="text/plain",
        status=200
    )


async def list_users(request: web.Request):
    return web.Response(
        body="list users",
        content_type="text/plain",
        status=200
    )


async def create_order(request: web.Request):
    return web.Response(
        body="create order",
        content_type="text/plain",
        status=200
    )


async def get_order(request: web.Request):
    return web.Response(
        body="get order",
        content_type="text/plain",
        status=200
    )


async def list_orders(request: web.Request):
    return web.Response(
        body="list orders",
        content_type="text/plain",
        status=200
    )


async def complete_orders(request: web.Request):
    return web.Response(
        body="complete orders",
        content_type="text/plain",
        status=200
    )


async def active_orders(request: web.Request):
    return web.Response(
        body="active orders",
        content_type="text/plain",
        status=200
    )


async def waiting_orders(request: web.Request):
    return web.Response(
        body="waiting orders",
        content_type="text/plain",
        status=200
    )


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
