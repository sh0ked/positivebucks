from abc import ABC, abstractmethod
from uuid import uuid4
from typing import Type


class BaseUser(ABC):
    uid: str
    name: str
    email: str

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError


class User:
    def __init__(self, uid: str = None, name: str = "UnnamedUser", email: str = None):
        self.uid = uid or str(uuid4())
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
        }


def get_user_impl() -> Type[User]:
    return User


BaseUser.register(User)
