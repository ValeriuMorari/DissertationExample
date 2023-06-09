"""Error handler layer"""
import logging

from enum import IntEnum, auto

# -------------------- logging init --------------------
LOGGER = logging.getLogger(__name__)
# set level to lowest prio i.e. DEBUG
LOGGER.setLevel(logging.DEBUG)


class ErrorHandler(Exception):
    # Set default message as None
    def __init__(self, message="Unknown exception"):
        super().__init__(message)
        # If Message -> PrintOut
        LOGGER.error('{}: {}'.format(
            self.__class__.__name__,
            message
        ))


class ErrorCode(IntEnum):
    NO_ERROR = auto()  # 1
    ERROR_1 = auto()  # 2
    ERROR_2 = auto()  # 3
    ERROR_3 = auto()  # 4
