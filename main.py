from logging_setup import LOGGER
import json
import copy
import argparse
from layers.interface_layer import InterfaceHandler


class TestExecutor:
    def __init__(self):
        self.interface_manager = InterfaceHandler()
        self.args = self.parse_args()

        with open("configuration.json") as f:
            self.configuration = json.load(f)
            self.tools = self.configuration["tools"]

    @staticmethod
    def parse_args():
        LOGGER.info("Parse all args...")
        arg_parser = argparse.ArgumentParser(description='Test Result Filter')

        arg_parser.add_argument('-tr', dest='tr_path',
                                help='test results path',
                                required=False)
        arg_parser.add_argument('-tc',
                                dest='test_cases',
                                help='test case list',
                                required=False)

        args = arg_parser.parse_args()
        args = vars(args)
        return args

    def initialize_interface_layer(self):
        LOGGER.info("Initialize interface layer...")
        for tool in self.configuration["tools"]:
            module_import = __import__("modules.%s.a_%s" % (tool, tool), fromlist=["Abstract%s" % tool])
            # Get Class Object
            module_class = getattr(module_import, 'Abstract%s' % tool)
            # Set Class as attribute for self, in order to be accessible from here
            setattr(self, tool, module_class(self.configuration[tool], copy.deepcopy(self.args)))
            # Share Interface manager
            self.__getattribute__(tool).interface_manager = self.interface_manager
            # Collect Interfaces
            self.interface_manager.collect(tool_name=tool, object_type=self.__getattribute__(tool))

    def initialize_tool_set(self):
        """
        Initialize all tools
        :return:
        """
        LOGGER.info("Initialize all tools...")
        for tool in self.tools:
            self.interface_manager.call(
                method_name="INIT",
                tool_name=tool,
                args=self.args
            )
        for tool in self.tools:
            self.interface_manager.call(
                method_name="PREPARE",
                tool_name=tool,
                args=self.args
            )

    def stop_tool_set(self):
        """
        Stop all tools
        :return:
        """
        LOGGER.info("Stop all tools...")
        for tool in self.tools:
            self.interface_manager.call(
                method_name="STOP",
                tool_name=tool,
                args=self.args
            )

    def keyword_read_dtc(self):
        """
        Read DTC keyword
        :return:
        """
        return self.interface_manager.call(method_name="dia.read_dtc")

    def keyword_send_diagnostic_request(self):
        """
        Send dia request DTC
        :return:
        """
        return self.interface_manager.call(method_name="dia.read_dtc")

    def run(self, tests: list):
        """
        Runner which run all tests
        :param tests:
        :return:
        """
        for test in tests:
            LOGGER.info("Start test case")
            for step in test:
                keyword = getattr(self, f"keyword_{step}")
                keyword()
            LOGGER.info("Stop test case")


if __name__ == "__main__":
    te = TestExecutor()
    te.initialize_interface_layer()
    te.initialize_tool_set()
    te.run([["read_dtc", "send_diagnostic_request"],
            ["send_diagnostic_request", "read_dtc"],
            ["read_dtc"]])
    te.stop_tool_set()
