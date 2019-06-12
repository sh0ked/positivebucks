from uuid import uuid4


class BaseUser:
    def __init__(self, uid: str = None, name: str = "Unnamed", email: str = None):
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


class User(BaseUser):
    pass


def get_user_impl() -> User:
    return User
