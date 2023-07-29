from core.logic_port import LogicPort
from core.logic_node import LogicNode
import uuid

class AddNode(LogicNode):

    NAME = "Add Node"

    def __init__(self):
        self._id = uuid.uuid4()
        self.default_value = 0.0
        self.node_color = (255, 152, 0)
        self.input_ports = self._create_inputs()
        self.output_ports = self._create_outputs()
        
    def _create_inputs(self):
        input_port_1 = LogicPort(is_input=True, parent_node=self, name="Input 1")
        input_port_2 = LogicPort(is_input=True, parent_node=self, name="Input 2")
        return {input_port_1.name : input_port_1, input_port_2.name : input_port_2}
    
    def _create_outputs(self):
        output_port = LogicPort(is_input=False, parent_node=self, name="Output")
        return {output_port.name : output_port}
    
    def _node_operation(self):
        try:
            self.output_ports.get("Output").data = float(self.input_ports.get("Input 1").data) + float(self.input_ports.get("Input 2").data)
        except:
            self.output_ports.get("Output").data = self.default_value
    
    def update(self):
        return self._node_operation()
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, new_id):
        self._id = new_id
