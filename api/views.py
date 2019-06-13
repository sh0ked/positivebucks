from aiohttp import web

from api.app import ApiApplication
from core.utils import is_int, json_to_str
from core.exceptions import UserNotFoundException, OrderCreationException, UserCreationException

HTTP_OK = 200
HTTP_CREATED = 201


class Request(web.Request):
    app: ApiApplication


async def _form_response(data: (dict, list), status_code: int = HTTP_OK) -> web.Response:
    """ Формирует ответ

    :param data:
    :param status_code:
    :return: Response
    """
    if isinstance(data, dict) or isinstance(data, list):
        content_type = "application/json"
        body = json_to_str(data).encode("utf-8")
    else:
        raise Exception(f"Unexpected '{type(data).__name__}' data type for response")

    return web.Response(
        body=body,
        content_type=content_type,
        status=status_code
    )


async def create_user(request: Request):
    """Создание нового клиента

    :param request:
    :return: Новый клиент
    """
    body = await request.json()

    name = body.get("name")
    if not name:
        raise UserCreationException(f"UID key wasn't found in {name}")

    email = body.get("email")
    if not email:
        raise UserCreationException(f"Email key wasn't found in {email}")

    user = await request.app.users.create(**{"name": name, "email": email})

    return await _form_response([user], status_code=HTTP_CREATED)


async def get_user(request: Request):
    """ Получить клиента по UID

    :param request:
    :return: Клиент по UID
    """
    uid = request.match_info.get("uid")
    result = await request.app.users.get(uid)

    return await _form_response(result)


async def list_users(request: Request):
    """Получение списка всех клиентов

    :param request:
    :return: Список всех клиентов
    """
    result = await request.app.users.all()

    return await _form_response(result)


async def create_order(request: Request):
    """Создание заказа

    :param request:
    :return: Список заказов ждущих приготовления
    """
    body = await request.json()
    user_uid, order_type = body.get("user_uid"), body.get("order_type")

    if not order_type or not is_int(order_type):
        raise OrderCreationException(f"Invalid order type: '{type(order_type)}'")

    if user_uid and not await request.app.users.user_is_exist(user_uid):
        raise UserNotFoundException(f"User with uid '{user_uid}' wasn't exist.")

    order_uid = await request.app.orders.create(user_uid=user_uid, order_type=order_type)
    return await _form_response({"uid": order_uid}, status_code=HTTP_CREATED)


async def get_order(request: Request):
    """Получение заказа по номеру

    :param request:
    :return: Заказ по номеру
    """
    order_uid = int(request.match_info.get("uid"))
    result = await request.app.orders.get(order_uid)

    return await _form_response(result)


async def list_orders(request: Request):
    """Получение списка всех заказов с полными данными о заказах

    :param request:
    :return: Список всех заказов с полными данными
    """
    result_dict = {
        "active": await request.app.orders.active(),
        "waiting": await request.app.orders.waiting(),
        "completed": await request.app.orders.completed(),
    }
    return await _form_response(result_dict)


async def table_orders(request: Request):
    """Табло заказов для клиентов

    :param request:
    :return:
    """
    active = await request.app.orders.pretty_active()
    waiting = await request.app.orders.pretty_waiting()
    completed = await request.app.orders.pretty_completed()

    active = [order for order in active]

    return await _form_response({
        "active": active,
        "waiting": waiting,
        "completed": completed,
    })


async def completed_orders(request: Request):
    """Получение списка выполненных заказов за последнюю минуту

    :param request:
    :return: Список выполненных заказов за последнюю минуту
    """
    result = await request.app.orders.completed()

    return await _form_response(result)


async def active_orders(request: Request):
    """Получение списка заказов в работе

    :param request:
    :return: Список заказов в работе
    """
    result = await request.app.orders.active()

    return await _form_response(result)


async def waiting_orders(request: Request):
    """Получение заказов ожидвющих выполнения

    :param request:
    :return: Список заказов ждущих приготовление
    """
    result = await request.app.orders.waiting()

    return await _form_response(result)


ROUTES = [
    web.post("/users", create_user),
    web.get("/users/{uid}", get_user),
    web.get("/users", list_users),
    web.post("/orders", create_order),
    web.get("/orders/{uid:\d+}", get_order),
    web.get("/orders", list_orders),
    web.get("/orders/table", table_orders),
    web.get("/orders/completed", completed_orders),
    web.get("/orders/active", active_orders),
    web.get("/orders/waiting", waiting_orders),
]
