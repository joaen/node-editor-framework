from core.logic_port import LogicPort
from core.logic_node import LogicNode
import uuid

class AddNode(LogicNode):

    NAME = "Add Node"

    def __init__(self):
        self.id = uuid.uuid4()
        self.default_value = 0.0
        self.node_color = (255, 152, 0)
        self.io_ports = self._create_ports()
        self.connections = []
        
    def _create_ports(self):
        input_port_1 = LogicPort(is_input=True, parent_node=self, name="Input 1", data=self.default_value)
        input_port_2 = LogicPort(is_input=True, parent_node=self, name="Input 2", data=self.default_value)
        output_port = LogicPort(is_input=False, parent_node=self, name="Output", data=self.default_value)
        return {input_port_1.name : input_port_1, input_port_2.name : input_port_2, output_port.name : output_port}
    
    def execute(self):
        try:
            self.io_ports.get("Output").data = float(self.io_ports.get("Input 1").data) + float(self.io_ports.get("Input 2").data)
        except:
            self.io_ports.get("Output").data = self.default_value
