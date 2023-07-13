from node.port import Port
from node.node import Node

class ExampleNode(Node):

    NAME = "Example Node"

    def __init__(self):
        self.exsists = True
        self.connections = {}
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()

    def _create_inputs(self):
        self.input_port_1 = Port(is_input=True, parent_node=self)
        self.input_port_2 = Port(is_input=True, parent_node=self)
        return {"Input 11" : self.input_port_1, "input 022" : self.input_port_2}
    
    def _create_outputs(self):
        self.output_port_1 = Port(is_input=False, parent_node=self)
        self.output_port_2 = Port(is_input=False, parent_node=self)
        return {"output11" : self.output_port_1, "output22" : self.output_port_2}

    def _node_operation(self):
        return super()._node_operation()
    
    def _update_connections(self):
        return super()._update_connections()
    
    def output(self):
        return super().output()

