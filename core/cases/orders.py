from typing import List
from datetime import timedelta

import settings
from core.utils import get_datetime_with_tz
from core.statuses import OrderStatuses
from core.storages import UsersStorage, OrdersStorage
from core.models.users import get_user_impl
from core.models.orders import get_order_impl


class Orders:
    def __init__(self, order_storage: OrdersStorage, user_storage: UsersStorage):
        self._order_storage = order_storage
        self._user_storage = user_storage

    async def list(self, filters: dict = None) -> List[dict]:
        """Получение списка всех заказов

        :return:
        """
        if filters:
            return await self._order_storage.list(filters=filters)
        return await self._order_storage.list()

    async def active(self) -> List[dict]:
        """Получеие списка заказов в работе

        :return:
        """
        return await self.list(filters={"status": OrderStatuses.ACTIVE.value})

    async def waiting(self) -> List[dict]:
        """Получение списка заказов, которые ожидают выполнения

        :return:
        """
        return await self.list(filters={"status": OrderStatuses.WAITING.value})

    async def completed(self) -> List[dict]:
        """Получение списка готовых заказов за последнюю минуту

        :return:
        """
        return await self.list(filters={
            "status": OrderStatuses.COMPLETED.value,
            "modified__gt": (get_datetime_with_tz() - timedelta(minutes=1)).timestamp()
        })

    async def _pretty_by_status(self, status: str):
        """Универсальный метод получения информации о заказах в красивом виде

        :param status:
        :return:
        """
        pretty_list = []
        orders_list = await self.list(filters={"status": status})
        for order_dict in orders_list:
            order_class = get_order_impl(order_dict.get("type"))
            order = order_class.from_dict(order_dict)

            pretty_order_info = {"order_uid": order.uid}
            if not order.user_uid:
                pretty_list.append(pretty_order_info)
                continue

            user_dict = await self._user_storage.list(filters={"uid": order.user_uid})
            if not user_dict:
                continue

            user_class = get_user_impl()
            user = user_class.from_dict(user_dict[0])
            pretty_order_info["user_name"] = user.name
            pretty_list.append(pretty_order_info)

        return pretty_list

    async def pretty_active(self) -> List[dict]:
        return await self._pretty_by_status(status=OrderStatuses.ACTIVE.value)

    async def pretty_waiting(self) -> List[dict]:
        return await self._pretty_by_status(status=OrderStatuses.WAITING.value)

    async def pretty_completed(self) -> List[dict]:
        return await self._pretty_by_status(status=OrderStatuses.COMPLETED.value)

    async def delete_outdated(self) -> List[str]:
        """Удаление устаревших готовых заказов из приложения

        :return:
        """
        results = await self._order_storage.list(filters={
            "status": OrderStatuses.COMPLETED.value,
            "modified__lt": (get_datetime_with_tz() - timedelta(
                minutes=settings.ORDERS_OUTDATE_LIMIT_IN_MINUTES)).timestamp()
        })
        return [await self._order_storage.delete(order_dict.get("uid")) for order_dict in results]

    async def get(self, order_uid: int) -> dict:
        """Получение заказа по UID (номеру)

        :param order_uid:
        :return:
        """
        orders_list = await self._order_storage.list(filters={"uid": order_uid})
        return orders_list[0] if len(orders_list) else None

    async def create(self, user_uid: str, order_type: int):
        """Создание нового заказа в приложении

        :param user_uid:
        :param order_type:
        :return:
        """
        order_uid = await self._order_storage.get_next_order_number()
        order_class = get_order_impl(order_type)
        order = order_class(uid=order_uid, user_uid=user_uid)
        await order.set_waiting_status()
        await self._order_storage.create(**order.to_dict())
        return order.uid

    async def update(self, order):
        """Обновление существующего заказа в приложении

        :param order:
        :return:
        """
        await order.set_modified()
        await self._order_storage.update(**order.to_dict())

    async def cook(self, order_uid: int):
        """Приготовление заказа по номеру

        :param order_uid:
        :return:
        """
        order_dict = await self.get(order_uid)
        order_class = get_order_impl(order_dict["type"])
        order = order_class.from_dict(order_dict)

        await order.set_active_status()
        await self.update(order)
        await order.cook()
        await order.set_completed_status()
        await self.update(order)
