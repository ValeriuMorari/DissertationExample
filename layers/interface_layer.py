import logging
from layers.error_handler import ErrorHandler, ErrorCode

# -------------------- logging init --------------------
LOGGER = logging.getLogger(__name__)
# set level to lowest prio i.e. DEBUG
LOGGER.setLevel(logging.DEBUG)


class InterfaceHandler(object):

    def __init__(self):

        # Interfaces dict template
        """
            interfaces = {
                interface_name: {
                    method
                }
            }
        """

        # All interfaces
        self.interfaces = {}

        # Tool interfaces dict Template
        """
            tool_name = {
                interface_name: {
                    method
                }
            }
        """
        self.tool_interfaces = {}

        """
            objectName->interfaceName: error_code
        """
        self.error_codes_stack = {}

    def collect(self, tool_name=None, object_type=None):
        """
        Collects all interfaces
        :param tool_name:
        :param object_type:
        :return:
        """
        LOGGER.info(f"Register: {tool_name}: {object_type}")
        # Check if object_type is an Object
        if not object_type or not isinstance(object_type, object):
            raise ValueError("Parameter: {} is not an object.".format(object_type))
        if not hasattr(object_type, 'interface_handler'):
            raise ValueError('Object: {} does not have attribute: interface_handler'.format(object_type))

        # Get object Name
        object_name = object_type.__class__.__name__ if not tool_name else tool_name

        # Get attribute 'interface_handler' from object_type
        object_interface_handler = object_type.__getattribute__('interface_handler')
        # If attribute is callable = method, call it
        if not callable(object_interface_handler):
            raise ValueError('Object: {} Attribute: interface_handler, is not callable'.format(object_type))

        # Call method - Except to return a dict
        object_interfaces = object_interface_handler()
        # Check if object_interfaces is not None and is dict
        if not object_interfaces or not isinstance(object_interfaces, dict):
            raise ValueError('Attribute: interface_handler of {}, return None or not dict'.format(object_name))
        # Add object to tool_interfaces
        self.tool_interfaces[object_name] = {}
        # Parse Interfaces
        for name, method in object_interfaces.items():
            # If interface is callable then store it
            if callable(object_interfaces[name]):
                # interface_method = object_interfaces[name]
                self.interfaces[name] = method
                self.tool_interfaces[object_name][name] = method
            else:
                raise ValueError('Attribute {} of {}, is not callable'.format(method, object_name))

    def call(self,
             method_name: str,
             tool_name: str = None,
             *args, **kwargs):
        """

        :param method_name:
        :param tool_name:
        :return:
        """
        if method_name and isinstance(method_name, str) and method_name in self.interfaces:
            if not tool_name:
                interface = self.interfaces[method_name]
            else:
                interface = self.tool_interfaces[tool_name][method_name]

            if callable(interface):
                LOGGER.info(f"Execute Interface -> '{interface.__self__}' - '{interface.__name__}'")
                result = interface(*args, **kwargs)
            else:
                LOGGER.error("Interface: {} is not callable".format(method_name))
                self.error_codes_stack.clear()
                self.error_codes_stack[method_name] = 'ErrorCode.INTERFACE_NOT_CALLABLE'
                raise ErrorHandler

        else:
            self.error_codes_stack.clear()
            self.error_codes_stack[method_name] = 'ErrorCode.INTERFACE_NOT_AVAILABLE'
            LOGGER.error("Interface: {} not available.".format(method_name))
            raise ErrorHandler

        # # Get Parent who did this call in order to clear 'error_code_stack'.
        # # In case that interfaces were called from modules, Keep 'error_code_stack' untouched
        if result is False:
            # Clear Stack before any new Read.
            self.error_codes_stack.clear()
            if hasattr(interface.__self__, 'ERROR_CODE'):
                # Collect ErrorCode
                error_code = interface.__self__.ERROR_CODE

                # Reset Error Code to avoid a wrong read on next operation
                interface.__self__.ERROR_CODE = ErrorCode.NO_ERROR

                # store error code
                self.error_codes_stack[method_name] = error_code

            raise ErrorHandler

    def all_interfaces(self, label=None):
        return list(self.interfaces)
