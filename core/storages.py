import asyncio
import logging
from typing import List

from core.utils import get_datetime_from_timestamp_with_tz
from core.exceptions import StorageException

log = logging.getLogger(__name__)


class BaseStorage:
    def __init__(self, entries: dict = None):
        self._entries = entries or {}
        self._lock = asyncio.Lock()

    @staticmethod
    async def _check(element_dict: dict, key: str, value) -> bool:
        """Проверка отношения значения фильтра и значения элемента. Больше, меньше, равно.

        :param element_dict:
        :param key:
        :param value:
        :return:
        """
        if "__" not in key:
            key = key + "__eq"

        key, operator = key.split("__")
        if operator not in ("eq", "lt", "gt"):
            raise ValueError(f"Operator {operator} is not supported")

        element_value = element_dict.get(key)
        if element_value and key in ("created", "modified"):
            element_value = get_datetime_from_timestamp_with_tz(element_value)
            value = get_datetime_from_timestamp_with_tz(value)

        if operator == "eq":
            return element_value == value

        if operator == "lt":
            return element_value < value

        if operator == "gt":
            return element_value > value

        return False


class UsersStorage(BaseStorage):

    async def list(self, filters: dict = None) -> List[dict]:
        """Получение списка клиентов с учетом фильтров

        :param filters:
        :return:
        """
        result = list(self._entries.values())

        if not filters:
            return result

        for key, value in filters.items():
            result = [element_dict for element_dict in result if await self._check(element_dict, key, value)]

        return result

    async def create(self, **user_dict) -> dict:
        """Создение нового клиента в хранилище

        :param user_dict:
        :return:
        """
        for user in self._entries.values():
            if user["email"] == user_dict["email"]:
                raise StorageException(f"User with the same email ({user_dict['email']}) was already existed.")

        with await self._lock:
            self._entries[user_dict["uid"]] = user_dict
        return user_dict


class OrdersStorage(BaseStorage):
    _last_order_number = 0

    async def get_next_order_number(self):
        """Возвращает следующий номер заказа для создания

        :return:
        """
        with await self._lock:
            self._last_order_number += 1
        return self._last_order_number

    async def list(self, filters: dict = None) -> List[dict]:
        """Получение списка заказов с учетом фильтров

        :param filters:
        :return:
        """
        result = list(self._entries.values())

        if not filters:
            return result

        for key, value in filters.items():
            result = [element for element in result if await self._check(element, key, value)]

        return result

    async def create(self, **order_dict) -> dict:
        """Создание заказа из набора атрибутов

        :param order_dict:
        :return:
        """
        order_uid = order_dict["uid"]
        if self._entries.get(order_uid):
            raise StorageException(f"Duplicate order was found with uid {order_uid}")

        with await self._lock:
            self._entries[order_uid] = order_dict
        return order_dict

    async def update(self, **order_dict) -> dict:
        """Обновление заказа в хранилище

        :param order_dict:
        :return:
        """
        order_uid = order_dict["uid"]

        with await self._lock:
            self._entries[order_uid] = order_dict
        return order_dict

    async def delete(self, order_uid: int) -> str:
        """Удаление заказа из хранилища

        :param order_uid:
        :return:
        """
        self._entries.pop(order_uid)
        log.info(f"Order #{order_uid} was deleted.")
        return str(order_uid)
