from node.port import Port
# from node.node import Node

class SumNode():

    def __init__(self):
        self._create_inputs()
        self._create_outputs()
        self._connections = dict()
        self._output_data = 0

    def create_connection(self, port_1: Port, port_2: Port):
        self._connections[port_2] = port_1
        print("this node is now connected to this node:")
        print(port_1.node)
        print(port_2.node)

    def break_connection(self, port_1: Port):
        port_2 = port_1.connection
        port_1.connection = None
        port_2.connection = None
        port_1.is_connected = False
        port_2.is_connected = False

    def _create_inputs(self):
        self.input_port_1 = Port(node=self)
        self.input_port_2 = Port(node=self)
    
    def _create_outputs(self):
        self.output_port_1 = Port(is_input=False, node=self)

    def _update_connections(self):
        for i in self._connections.values():
            self._output_data += i.data

    def output(self):
        self._update_connections()
        return self._output_data

