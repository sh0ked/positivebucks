from typing import List

from core.models.users import User
from core.storages import UsersStorage
from core.exceptions import UserCreationException


class Users:
    def __init__(self, storage: UsersStorage):
        self._storage = storage

        import asyncio
        asyncio.ensure_future(self.create(**{
            "name": "Алешка",
            "email": "test@test.ru",
        }))

    async def all(self) -> List[dict]:
        """Получение списка всех клиентов

        :return:
        """
        return await self._storage.list()

    async def get(self, uid: str) -> List[dict]:
        """Получение клиента по UID

        :param uid:
        :return:
        """
        return await self._storage.list(filters={"uid": uid})

    async def user_is_exist(self, user_uid: str) -> bool:
        """Проверка существования клиента по UID

        :param user_uid:
        :return:
        """
        user_list = await self.get(user_uid)
        return bool(len(user_list))

    async def create(self, **user_dict) -> dict:
        """Создание клиента в приложении

        :param user_dict:
        :return:
        """
        name = user_dict.get("name")
        if not name:
            raise UserCreationException(f"UID key wasn't found in {name}")

        email = user_dict.get("email")
        if not email:
            raise UserCreationException(f"Email key wasn't found in {email}")

        user = User.from_dict(user_dict)
        return await self._storage.create(**user.to_dict())
