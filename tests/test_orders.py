from core.models.orders import Order


def test_user_init():
    uid, name = 0, "TestOrder"
    user = Order(uid=uid)

    assert user.uid == uid


def test_user_from_dict():
    data = {
        "uid": 0,
        "name": "TestOrder",
    }
    user = Order.from_dict(data)

    assert user.uid == data["uid"]
    assert user.name == data["name"]
