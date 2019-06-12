import logging
import asyncio
from aiohttp import web

from core.queue import OrdersQueue
from core.cases.users import Users
from core.cases.orders import Orders
from core.storages import UsersStorage, OrdersStorage


log = logging.getLogger(__name__)


class ApiApplication(web.Application):
    """
    Основное приложение реализующее обработку заказов и предоставляющее API
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_storage = UsersStorage()
        orders_storage = OrdersStorage()
        self.users = Users(user_storage)
        self.orders = Orders(orders_storage, user_storage)
        self.queue = OrdersQueue(self.orders)

        self.on_startup.append(self.startup_func)
        self.on_cleanup.append(self.cleanup_func)
        self.on_shutdown.append(self.shutdown_func)

    async def startup_func(self, app):
        log.info("Starting app...")
        asyncio.ensure_future(self.queue.run())

    async def cleanup_func(self, app):
        log.info("Cleanup in progress...")

    async def shutdown_func(self, app):
        log.info("Shutting down...")
        await self.queue.stop()


def create_app():
    """Функция создание API-приложения

    :return:
    """
    from api import middlewares
    from api.views import ROUTES as API_ROUTES

    api_app = ApiApplication(
        middlewares=[
            middlewares.request_middleware
        ],
    )
    api_app.router.add_routes(API_ROUTES)

    return api_app
