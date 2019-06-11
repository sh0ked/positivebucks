import ujson


def json_to_str(data, ensure_ascii=True, indent=0, sort_keys=False) -> str:
    return ujson.dumps(data, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys)
