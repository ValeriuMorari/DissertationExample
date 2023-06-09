# --- Imports
import logging

# --- from Imports

# --- Project specific Imports
from modules.generic_application_module import GenericApp
from modules.DiagnosticsVW.b_DiagnosticsVW import BaseDiagnosticsVW
from layers.error_handler import ErrorCode

# -------------------- logging init --------------------
LOGGER = logging.getLogger(__name__)
# set level to lowest prio i.e. DEBUG
LOGGER.setLevel(logging.DEBUG)


# Naming Rule: a_name
class AbstractDiagnosticsVW(GenericApp):
    # ------------------------------------------------------------------------------------------------------------------
    # Mandatory Inputs
    # ------------------------------------------------------------------------------------------------------------------
    PATH_INPUTS = []
    MANDATORY_INPUTS = [
        'attr1',
        'attr2'
    ]

    # ------------------------------------------------------------------------------------------------------------------
    # Interfaces
    # ------------------------------------------------------------------------------------------------------------------
    INTERFACE_INIT = "INIT"
    INTERFACE_PREPARE = "PREPARE"
    INTERFACE_STOP = "STOP"
    SEND_DIA_REQ = "dia.diagnostic_request"
    READ_DTC = "dia.read_dtc"

    # ------------------------------------------------------------------------------------------------------------------
    # Required Interfaces
    # ------------------------------------------------------------------------------------------------------------------
    REQ_INTERFACES = [
    ]

    def __init__(self, tool_config=None, run_args=None):
        """

        :param tool_config:
        :param run_args:
        """
        # run app. module constructor
        super(AbstractDiagnosticsVW, self).__init__()

        # template constructor
        self.base_module = None

        self.tool_config = tool_config
        self.args = run_args

    def interface_handler(self):
        """
        Collection of abstract interfaces
        :return:
        """
        interfaces = {
            self.INTERFACE_INIT:    self.interface_init,
            self.INTERFACE_STOP:    self.interface_stop,
            self.INTERFACE_PREPARE: self.interface_prepare,
            self.SEND_DIA_REQ:   self.interface_send_diagnostic_request,
            self.READ_DTC: self.interface_read_dtc
        }
        return interfaces

    def interface_init(self, args=None):
        """
        Mandatory initialization interface
        :param args:
        :return:
        """

        if args is None:
            args = self.args

        # CROSS CHECK EXISTANCE OF METHODS FROM OTHER MODULES IF NEEDED
        missing_interfaces = set(self.REQ_INTERFACES) - set(self.interface_manager.interfaces.keys())
        if missing_interfaces:
            LOGGER.error(
                "Missing Interfaces. There are no tools to provide interfaces: {}".format(missing_interfaces)
            )
            return False

        if self.check_key(self.tool_config) is False:
            LOGGER.info("template initialization fails")
            return False

        if self.check_paths(self.tool_config) is False:
            LOGGER.error("template initialization fails")
            return False

        LOGGER.info("Initialize base module")
        self.base_module = BaseDiagnosticsVW(
            attr1="some_path",
            attr2="351",
            attr3=None
        )

        if self.base_module.base_module_init is False:
            return False
        else:
            return True

    def interface_prepare(self, args=None):
        """
        Mandatory prepare interface
        :param args:
        :return:
        """
        pass

    def interface_stop(self, args=None):
        """
        Mandatory stop interface
        :param args:
        :return:
        """
        pass

    def interface_send_diagnostic_request(self):
        """
        Interface aimed to send DiagnosticsVW request
        :return:
        """
        self.base_module.base_event()
        self.base_module.base_event_2()

    def interface_read_dtc(self):
        """
        Interface aimed to read DTC
        :return:
        """
        self.base_module.base_event()
        self.base_module.base_event_2()

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__
