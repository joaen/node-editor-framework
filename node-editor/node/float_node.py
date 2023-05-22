from node.port import Port
# from node.node import Node

class FloatNode():

    def __init__(self, number):
        self._create_outputs()
        self.connections = dict()
        self._float = number 
    
    def _create_outputs(self):
        self.output_port = Port(is_input=False, node=self)

    @property
    def output(self):
        self.output_port.data = self._float
        return self.output_port

