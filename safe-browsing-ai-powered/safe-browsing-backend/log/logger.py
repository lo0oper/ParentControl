import sys
import logging
import os 

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Set a default value if variable is not found

logger = logging.getLogger("middlewareLogger")
stdout = logging.StreamHandler(stream=sys.stdout)

fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d ::  %(message)s"
)

stdout.setFormatter(fmt)
logger.addHandler(stdout)

# Set log level based on the environment variable
log_levels = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

logger.setLevel(log_levels.get(LOG_LEVEL.upper(), logging.INFO))
