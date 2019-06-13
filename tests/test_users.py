from uuid import uuid4

from core.models.users import User, BaseUser


def test_user_init():
    uid, name, email = str(uuid4()), "TestUser", "test@test.ru"
    user = User(uid=uid, name=name, email=email)

    assert isinstance(user, BaseUser)
    assert user.uid == uid
    assert user.name == name
    assert user.email == email


def test_user_from_dict():
    data = {
        "uid": str(uuid4()),
        "name": "TestUser",
        "email": "test@test.ru"
    }
    user = User.from_dict(data)

    assert isinstance(user, BaseUser)
    assert user.uid == data["uid"]
    assert user.name == data["name"]
    assert user.email == data["email"]

# так мало потому, что просто пример
