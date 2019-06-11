import logging
from envparse import env, logger

log = logging.getLogger(__name__)
env_logger = logger.setLevel("WARNING")

# logging
LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")
THIRD_PARTY_LOG_LEVEL = env.str("THIRD_PARTY_LOG_LEVEL", default="WARNING")

# api
APP_HOST = env.str("APP_HOST", default="0.0.0.0")
APP_PORT = env.int("APP_PORT", default=8000)
ACCESS_CONTROL_ALLOW_ORIGIN = env.str("ACCESS_CONTROL_ALLOW_ORIGIN", default="*")
ACCESS_CONTROL_ALLOW_HEADERS = env.str("ACCESS_CONTROL_ALLOW_HEADERS", default="*")
