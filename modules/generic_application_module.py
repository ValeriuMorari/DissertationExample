"""Generic application class which contains common methods"""
import logging
import os
from layers.error_handler import ErrorCode
# -------------------- logging init --------------------
LOGGER = logging.getLogger(__name__)
# set level to lowest prio i.e. DEBUG
LOGGER.setLevel(logging.DEBUG)


class GenericApp:
    # --- Default Interfaces ------------------
    INIT = "INIT"
    PREPARE = "PREPARE"
    STOP = "STOP"
    # -----------------------------------------

    # --- Required Interfaces ------------------
    # This List should be overwritten by module who inherit this object, and populate with the needed interface names
    REQ_INTERFACES = []
    REQ_INTERFACES_LABEL_SPECIFIC = []
    # ------------------------------------------

    # --- Mandatory Inputs ---------------------
    # This list should contain necessary parameters that are mandatory to be present in configuration file
    MANDATORY_INPUTS = []
    # ------------------------------------------

    # --- Path Inputs --------------------------
    PATH_INPUTS = []
    # ------------------------------------------

    # --- Tool Version Control -----------------
    TOOL_VERSION_MAX = None
    TOOL_VERSION_MIN = None
    # ------------------------------------------

    # --- Workspace ----------------------------
    # Needed for all modules to know where to store additional files (log, temporary files, measurements.)
    WORKSPACE = None

    # ------------------------------------------

    def __init__(self):
        # Interface Manager
        self.interface_manager = None

        # Get Parent
        self.parent = self.__class__.__name__

        # Marker which tells whether module is initialized
        self.initialized = False

        # Generic error code
        self.ERROR_CODE = ErrorCode.NO_ERROR

    def check_paths(self, tool_config):
        """

        :param tool_config:
        :return:
        """

        # Vars
        result_list = []

        if not tool_config:
            LOGGER.error("[{}] Parameter 'tool_config' was not provided.".format(self.parent))
            return False

        for path in self.PATH_INPUTS:
            if path not in tool_config:
                LOGGER.error("[{}] Parameter '{}' is not present in 'tool_config'.".format(self.parent, path))
                result_list.append(False)

            elif not tool_config[path] or not os.path.exists(str(tool_config[path])):
                LOGGER.error(
                    "[{}] Provided path for parameter '{}' in tool_config is not found: {}".format(
                        self.parent,
                        path,
                        tool_config[path]
                    )
                )
                result_list.append(False)
            else:
                LOGGER.debug("[{}] Path: {} was found".format(self.parent, tool_config[path]))
                result_list.append(True)

        if False in result_list:
            return False
        else:
            return True

    def check_key(self, tool_config):
        """
        check if key list is present in dictionary
        :param tool_config:
        :return:
        """

        result_list = []

        if not tool_config:
            LOGGER.error("[{}] Parameter 'tool_config' was not provided.".format(self.parent))
            return False

        for key in self.MANDATORY_INPUTS:
            if key in tool_config.keys():
                LOGGER.debug("[{}] Input: '{}' found successfully.".format(self.parent, key))
                result_list.append(True)
            else:
                LOGGER.error("[{}] Input: '{}' was not found. Please update "
                             "configuration.json with missing input: '{}'".format(self.parent, key, key))
                result_list.append(False)

        if False in result_list:
            self.initialized = False
            return False
        else:
            return True

    def uppercase_for_dict(self, lower_dict):
        """
        Convert all dictionary to upper case
        :param lower_dict:
        :return:
        """
        upper_dict = {}
        for k, v in lower_dict.items():
            if isinstance(v, dict):
                v = self.uppercase_for_dict(v)
            upper_dict[k.upper().strip()] = str(v).upper().strip()

        return upper_dict

    @staticmethod
    def check_version(current_version, min_version, max_version):
        """

        :param current_version:
        :param min_version:
        :param max_version:
        :return:
        """
        verdict = True
        current_version = current_version.split(".")
        min_version = min_version.split(".")
        max_version = max_version.split(".")

        iterrations = max(current_version, min_version, max_version)

        for i in range(iterrations):
            if current_version[i] > max_version[i]:
                verdict = False
            if current_version[i] < min_version[i]:
                verdict = False

        return verdict
