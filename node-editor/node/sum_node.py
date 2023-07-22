from node.port import Port
from node.node import Node

class SumNode(Node):

    NAME = "Sum Node"

    def __init__(self):
        self.exsists = True
        self.connections = {}
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()
        
    def _create_inputs(self):
        self.input_port_1 = Port(is_input=True, parent_node=self)
        self.input_port_2 = Port(is_input=True, parent_node=self)
        return {"X (Float)" : self.input_port_1, "Y (Float)" : self.input_port_2}
    
    def _create_outputs(self):
        self.output_port_1 = Port(is_input=False, parent_node=self)
        return {"Output" : self.output_port_1}
    
    def _node_operation(self):
        self.output_port_1.data = int(self.input_port_1.data) + int(self.input_port_2.data)
    
    def update(self):
        return self._node_operation()
    
    def output(self):
        return self.output_port_1.data
