import logging
from envparse import env, logger

log = logging.getLogger(__name__)
env_logger = logger.setLevel("WARNING")

# logging
LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")
THIRD_PARTY_LOG_LEVEL = env.str("THIRD_PARTY_LOG_LEVEL", default="WARNING")
