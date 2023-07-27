from core.logic_port import LogicPort
from core.logic_node import LogicNode

class FloatNode(LogicNode):

    NAME = "Float Node"

    def __init__(self):
        self.exsists = True
        self.default_value = 0.0
        self.node_color = (0, 169, 244)
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()
        self.output_port = None

    def _node_operation(self):
        try:
            self.output_port.data = float(self.input_port.data)
        except:
            self.output_port.data = self.default_value
    
    def update(self):
        self._node_operation()
    
    def _create_inputs(self):
        self.input_port = LogicPort(is_input=True, parent_node=self)
        input_dict = {"Input" : self.input_port}
        return input_dict
    
    def _create_outputs(self):
        self.output_port = LogicPort(is_input=False, parent_node=self)
        output_dict = {"Output" : self.output_port}
        return output_dict


