from node.port import Port
from node.node import Node

class MultiplyNode(Node):

    NAME = "Multiply Node"

    def __init__(self):
        self.default_value = 0.0
        self.exsists = True
        self.connections = {}
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()
        
    def _create_inputs(self):
        self.input_port_1 = Port(is_input=True, parent_node=self)
        self.input_port_2 = Port(is_input=True, parent_node=self)
        return {"Input 1" : self.input_port_1, "Input 2" : self.input_port_2}
    
    def _create_outputs(self):
        self.output_port_1 = Port(is_input=False, parent_node=self)
        return {"Output" : self.output_port_1}
    
    def _node_operation(self):
        try:
            self.output_port_1.data =  round(float(self.input_port_1.data) * float(self.input_port_2.data), 3)
        except:
            self.output_port_1.data = self.default_value
    
    def update(self):
        return self._node_operation()
    
    def output(self):
        return self.output_port_1.data
