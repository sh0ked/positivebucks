import asyncio
import logging
from enum import Enum
from datetime import datetime

from core.utils import get_datetime_with_tz, get_datetime_from_timestamp_with_tz
from core.statuses import OrderStatuses
from core.exceptions import OrderCreationException

log = logging.getLogger(__name__)


class CoffeeTypes(Enum):
    UNKNOWN = 0
    CAPPUCINO = 1
    AMERICANO = 2


class Order:
    name: str = "Unnamed Order"
    cook_time: int = 1

    def __init__(self, uid: int = 0, status: int = OrderStatuses.UNKNOWN.value,
                 user_uid: int = None, created: datetime = None, modified: datetime = None):
        self.uid = uid
        self._status = status
        self.user_uid = user_uid
        self.created = created or get_datetime_with_tz()
        self._modified = modified or get_datetime_with_tz()

    @property
    def type(self):
        raise NotImplementedError

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
        raise NotImplementedError

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


class Coffee(Order):
    name: str = "Unnamed Coffee"

    @property
    def type(self):
        return CoffeeTypes.UNKNOWN.value

    async def _cook(self):
        await asyncio.sleep(self.cook_time)


class Cappucino(Coffee):
    name: str = "Cappucino"
    cook_time = 20

    @property
    def type(self):
        return CoffeeTypes.CAPPUCINO.value


class Americano(Coffee):
    name: str = "Americano"
    cook_time = 10

    @property
    def type(self):
        return CoffeeTypes.AMERICANO.value


def get_order_impl(order_type: int) -> (Cappucino, Americano):
    if order_type == CoffeeTypes.CAPPUCINO.value:
        return Cappucino

    if order_type == CoffeeTypes.AMERICANO.value:
        return Americano

    raise OrderCreationException(f"Order with type {order_type} wasn't found.")
