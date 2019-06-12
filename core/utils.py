import ujson
import logging
from datetime import datetime, timezone


log = logging.getLogger(__name__)


def json_to_str(data, ensure_ascii=True, indent=0, sort_keys=False) -> str:
    """Конвертация JSON в строку

    :param data:
    :param ensure_ascii:
    :param indent:
    :param sort_keys:
    :return:
    """
    return ujson.dumps(data, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys)


def get_datetime_with_tz() -> datetime:
    """Получение текущей даты и времени с учетом локальной таймзоны

    :return:
    """
    return datetime.now(timezone.utc).astimezone()


def get_datetime_from_timestamp_with_tz(timestamp: float) -> datetime:
    """Получение даты и времени из unix timestamp

    :param timestamp:
    :return:
    """
    try:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone()
    except:
        log.exception(f"Unable date getting from {timestamp}")


def is_int(value, except_return=None):
    """Проверка на integer

    :param value:
    :param except_return:
    :return:
    """
    try:
        return int(value)
    except ValueError:
        return except_return
