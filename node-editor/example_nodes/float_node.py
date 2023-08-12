from core.logic_port import LogicPort
from core.logic_node import LogicNode
import uuid

class FloatNode(LogicNode):

    NAME = "Float Node"

    def __init__(self):
        self.id = uuid.uuid4()
        self.default_value = 0.0
        self.node_color = (0, 169, 244)
        self.io_ports = self._create_ports()
        self.connections = []

    def _create_ports(self):
        input_port = LogicPort(is_input=True, parent_node=self, name="Input", data=self.default_value)
        output_port = LogicPort(is_input=False, parent_node=self, name="Output", data=self.default_value)
        input_dict = {input_port.name : input_port, output_port.name : output_port}
        return input_dict

    def execute(self):
        try:
            self.io_ports.get("Output").data = float(self.io_ports.get("Input").data)
        except:
            self.io_ports.get("Output").data = self.default_value

