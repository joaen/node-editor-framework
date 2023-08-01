from core.logic_port import LogicPort
from core.logic_node import LogicNode
import uuid

class FloatNode(LogicNode):

    NAME = "Float Node"

    def __init__(self):
        self._id = uuid.uuid4()
        self.default_value = 0.0
        self.node_color = (0, 169, 244)
        self.input_ports = self._create_inputs()
        self.output_ports = self._create_outputs()
        self.connections = []

    def _node_operation(self):
        try:
            self.output_ports.get("Output").data = float(self.input_ports.get("Input").data)
        except:
            self.output_ports.get("Output").data = self.default_value
    
    def update(self):
        self._node_operation()
    
    def _create_inputs(self):
        input_port = LogicPort(is_input=True, parent_node=self, name="Input", data=self.default_value)
        input_dict = {input_port.name : input_port}
        return input_dict
    
    def _create_outputs(self):
        output_port = LogicPort(is_input=False, parent_node=self, name="Output", data=self.default_value)
        output_dict = {output_port.name : output_port}
        return output_dict
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id):
        self._id = new_id


