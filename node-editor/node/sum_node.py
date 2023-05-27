from node.port import Port
from node.node import Node

class SumNode(Node):

    def __init__(self):
        super().__init__()
        self._create_inputs()
        self._create_outputs()
        # self._connections = dict()
        self._output_data = 0

    def _create_inputs(self):
        self.input_port_1 = Port(node=self)
        self.input_port_2 = Port(node=self)
    
    def _create_outputs(self):
        self.output_port_1 = Port(is_input=False, node=self)

    def _update_connections(self):
        try:
            self.input_port_1.data = self.input_port_1.connection.data
            self.input_port_2.data = self.input_port_2.connection.data
            self._output_data = (self.input_port_1.data + self.input_port_2.data)
        except:
            self._output_data = 0

    def output(self):
        self._update_connections()
        return self._output_data

