import logging
import traceback

from aiohttp import web
from aiohttp.web_exceptions import HTTPError

import settings
from core.utils import json_to_str


log = logging.getLogger(__name__)


def _form_error_response(
    user_message: str, status_code: int, internal_message: str = None
):
    """Функция для формирования ответа с ошибками

    :param user_message:
    :param status_code:
    :param internal_message:
    :return:
    """
    body = {
        "errors": [
            {
                "message": user_message,
                "internal_message": internal_message,
            }
        ]
    }
    return web.Response(
        body=json_to_str(body).encode("utf-8"),
        content_type="application/json",
        status=status_code
    )


async def request_middleware(app, handler):
    """Прослойка для отлова базовых ошибок

    :param app:
    :param handler:
    :return:
    """
    async def middleware(request):
        try:
            response = await handler(request)
        except HTTPError as e:
            response = _form_error_response(
                user_message=e.reason,
                status_code=e.status_code
            )
        except:
            log.exception("Unexpected exception")
            response = _form_error_response(
                user_message="Sorry, the internal server error",
                internal_message=traceback.format_exc(),
                status_code=500
            )

        log.info(f"{request.method} {request.path}{request.query_string}")
        response.headers.add("Access-Control-Allow-Origin", settings.ACCESS_CONTROL_ALLOW_ORIGIN)
        response.headers.add("Access-Control-Allow-Headers", settings.ACCESS_CONTROL_ALLOW_HEADERS)
        return response

    return middleware
