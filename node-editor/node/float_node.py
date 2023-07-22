from node.port import Port
from node.node import Node

class FloatNode(Node):

    NAME = "Float Node"

    def __init__(self):
        self.exsists = True
        self.connections = None
        self.output_port = None
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()

    def _node_operation(self):
        self.output_port.data = self.input_port.data
    
    def update(self):
        self._node_operation()
    
    def _create_inputs(self):
        self.input_port = Port(is_input=True, parent_node=self)
        input_dict = {"Input" : self.input_port}
        return input_dict
    
    def _create_outputs(self):
        self.output_port = Port(is_input=False, parent_node=self)
        output_dict = {"Output" : self.output_port}
        return output_dict

    def output(self):
        return super().output()



