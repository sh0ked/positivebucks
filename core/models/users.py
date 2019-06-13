from uuid import uuid4
from typing import Type

from core.models.bases import BaseUser


class User(BaseUser):
    def __init__(self, uid: str = None, name: str = "UnnamedUser", email: str = None):
        self._uid = uid or str(uuid4())
        self._name = name
        self._email = email

    @property
    def uid(self):
        return self._uid

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
        }


def get_user_impl() -> Type[BaseUser]:
    return User
