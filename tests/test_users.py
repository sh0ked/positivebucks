from uuid import uuid4

from core.models.users import User


def test_user_init():
    uid, name, email = str(uuid4()), "TestUser", "test@test.ru"
    user = User(uid=uid, name=name, email=email)

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

    assert user.uid == data["uid"]
    assert user.name == data["name"]
    assert user.email == data["email"]
