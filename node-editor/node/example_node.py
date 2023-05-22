from node.port import Port
# from node.node import Node

class ExampleNode():

    def __init__(self):
        self._create_inputs()
        self._create_outputs()
        self.connections = dict()

    def create_connection(self, port_1: Port, port_2: Port):
        self.connections[port_2] = port_1
        # port_2.data = port_1.data
        # port_1.connection = port_2
        # port_2.connection = port_1
        # port_1.is_connected = True
        # port_2.is_connected = True
    def update_connections(self):
        # port_2.data = port_1.data
        # pass
        for i in self.connections.keys():
            # i = self.connections.get(i)
            # print(i)
            i.data = self.connections.get(i).data
            # print(self.connections.get(i))
            # print(i)

    def break_connection(self, port_1: Port):
        port_2 = port_1.connection
        port_1.connection = None
        port_2.connection = None
        port_1.is_connected = False
        port_2.is_connected = False

    def _create_inputs(self):
        self.input_port_1 = Port()
        self.input_port_2 = Port()
    
    def _create_outputs(self):
        self.output_port_1 = Port(is_input=False)
        self.output_port_2 = Port(is_input=False)

    @property
    def output_1(self):
        self.output_port_1.data = (self.input_port_1.data * self.input_port_2.data)
        return self.output_port_1.data
    
    @property
    def output_2(self):
        self.output_port_2.data = (self.input_port_1.data + self.input_port_2.data)
        return self.output_port_2.data

