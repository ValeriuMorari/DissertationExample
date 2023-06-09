import json
import logging.config


# -------------------- logging init --------------------
with open("logging_config.json") as file:
    log_config = json.load(file)

# Configure the logger using the configuration dictionary
logging.config.dictConfig(log_config)

LOGGER = logging.getLogger(__name__)

# set level to lowest prio i.e. DEBUG
LOGGER.setLevel(logging.DEBUG)

LOGGER.debug("Debug message")
LOGGER.info("Info message")
LOGGER.warning("Warning message")
LOGGER.error("Error message")