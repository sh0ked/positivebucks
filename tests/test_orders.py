from core.models.bases import BaseOrder
from core.models.orders import Cappucino


def test_user_init():
    uid, name = 0, "Cappucino"
    user = Cappucino(uid=uid)

    assert isinstance(user, BaseOrder)
    assert user.uid == uid
    assert user.name == name


def test_user_from_dict():
    data = {
        "uid": 0,
        "name": "Cappucino",
    }
    user = Cappucino.from_dict(data)

    assert isinstance(user, BaseOrder)
    assert user.uid == data["uid"]
    assert user.name == data["name"]

# так мало потому, что просто пример
