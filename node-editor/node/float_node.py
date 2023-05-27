from node.port import Port
from node.node import Node

class FloatNode(Node):

    def __init__(self, number):
        super().__init__()
        self._create_outputs()
        self.connections = dict()
        self.output_port.data = number
    
    def _create_outputs(self):
        self.output_port = Port(is_input=False, node=self)

