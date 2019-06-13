from abc import ABC, abstractmethod


class BaseUser(ABC):
    @property
    def uid(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def email(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError


class BaseOrder(ABC):
    @property
    @abstractmethod
    def uid(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def cook_time(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def user_uid(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def created(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def modified(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    async def status(self):
        raise NotImplementedError

    @abstractmethod
    async def cook(self):
        raise NotImplementedError

    @abstractmethod
    async def _cook(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError
