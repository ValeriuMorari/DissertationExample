# --- Imports
import logging
import os

# --- from Imports

# -------------------- logging init --------------------
LOGGER = logging.getLogger(__name__)
# set level to lowest prio i.e. DEBUG
LOGGER.setLevel(logging.DEBUG)


# Naming Rule: BaseName.
class BaseDiagnosticsVW(object):

    def __init__(
            self,
            attr1: str = None,
            attr2: str = None,
            attr3: str = None,
    ):
        """
        Doc String
        :param attr1:
        :param attr2:
        :param attr3:
        """
        # ---------------- initialize class attributes  ----------------

        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

    def base_module_init(self):
        """
        Initialize module
        :return:
        """
        # ---------------- plausibility check ----------------
        if not self.attr1:
            # Print Message Here
            return False
        if not os.path.isfile(self.attr2):
            # Print Message Here
            return False
        if not self.attr3:
            # Print Message Here
            return False

        return True

    def base_event(self):
        """

        :return:
        """

        pass

    def base_event_2(self):
        """

        :return:
        """
        pass

    def base_event_3(self):
        """

        :return:
        """
        pass

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__
