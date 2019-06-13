import asyncio
import logging

from enum import Enum
from typing import Type
from datetime import datetime

from core.models.bases import BaseOrder
from core.utils import get_datetime_with_tz, get_datetime_from_timestamp_with_tz
from core.statuses import OrderStatuses
from core.exceptions import OrderCreationException

log = logging.getLogger(__name__)


class CoffeeTypes(Enum):
    UNKNOWN = 0
    CAPPUCINO = 1
    AMERICANO = 2


class Coffee(BaseOrder):
    _name: str = "Unnamed Coffee"
    _cook_time: int = 1

    def __init__(self, uid: int = 0, status: int = OrderStatuses.UNKNOWN.value,
                 user_uid: int = None, created: datetime = None, modified: datetime = None):
        self._uid = uid
        self._status = status
        self._user_uid = user_uid
        self._created = created or get_datetime_with_tz()
        self._modified = modified or get_datetime_with_tz()

    @property
    def uid(self):
        return self._uid

    @property
    def cook_time(self):
        return self._cook_time

    @property
    def name(self):
        return self._name

    @property
    def user_uid(self):
        return self._user_uid

    @property
    def type(self):
        raise CoffeeTypes.UNKNOWN.value

    @property
    def created(self):
        return self._created

    @property
    def modified(self):
        return self._modified

    async def set_modified(self):
        self._modified = get_datetime_with_tz()

    @property
    def status(self):
        return self._status

    async def _set_status(self, status: int):
        log.debug(f"Order '{self.name}' #{self.uid} in status '{status}'.")
        self._status = status

    async def set_active_status(self):
        """Установка статуса "в процессе"

        :return:
        """
        await self._set_status(OrderStatuses.ACTIVE.value)

    async def set_waiting_status(self):
        """Установка статуса "ожидания"

        :return:
        """
        await self._set_status(OrderStatuses.WAITING.value)

    async def set_completed_status(self):
        """Установка статуса заказа "выполнен"

        :return:
        """
        await self._set_status(OrderStatuses.COMPLETED.value)

    async def cook(self):
        """Выполнить операцию приготовления заказа

        :return:
        """
        log.info(f"Order '{self.name}' #{self.uid} is cooking for {self.cook_time} seconds...")
        await self._cook()
        log.info(f"Order '{self.name}' #{self.uid} was completed.")

    async def _cook(self):
        await asyncio.sleep(self.cook_time)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            uid=data.get("uid"),
            status=data.get("status"),
            user_uid=data.get("user_uid"),
            created=get_datetime_from_timestamp_with_tz(data.get("created"))
            if data.get("created") else get_datetime_with_tz(),
            modified=get_datetime_from_timestamp_with_tz(data.get("modified"))
            if data.get("modified") else get_datetime_with_tz()
        )

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "type": self.type,
            "cook_time": self.cook_time,
            "status": self.status,
            "user_uid": self.user_uid,
            "created": self.created.timestamp(),
            "modified": self.modified.timestamp()
        }


class Cappucino(Coffee):
    _name: str = "Cappucino"
    _cook_time = 20

    @property
    def type(self):
        return CoffeeTypes.CAPPUCINO.value


class Americano(Coffee):
    _name: str = "Americano"
    _cook_time = 10

    @property
    def type(self):
        return CoffeeTypes.AMERICANO.value


def get_order_impl(order_type: int) -> Type[Coffee]:
    if order_type == CoffeeTypes.CAPPUCINO.value:
        return Cappucino

    if order_type == CoffeeTypes.AMERICANO.value:
        return Americano

    raise OrderCreationException(f"Order with type {order_type} wasn't exist for creating.")
