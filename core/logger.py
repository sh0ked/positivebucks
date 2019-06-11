import logging


def _setup_logging(log_level=logging.INFO, third_party_log_level=logging.WARNING):
    logging.basicConfig(level=log_level, format=logging.BASIC_FORMAT)
    for logger in ["aiohttp.access"]:
        logging.getLogger(logger).setLevel(third_party_log_level)


def setup_loggers(log_level, third_party_log_level):
    _setup_logging(log_level, third_party_log_level)
