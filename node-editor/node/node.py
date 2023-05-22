# from abc import ABC, abstractmethod
# from node.port import Port

# class Node():

#     def __init__(self):
#         self.create_inputs()
#         self.create_outputs()
#         # self.connections = {}

#     def create_connection(self, port_1: Port, port_2: Port):
#         port_1.connection = port_2
#         port_2.connection = port_1
#         port_1.is_connected = True
#         port_2.is_connected = True
#         # self.connections[port_1] = port_2

#     def break_connection(self, port_1: Port):
#         port_2 = port_1.connection
#         port_1.connection = None
#         port_2.connection = None
#         port_1.is_connected = False
#         port_2.is_connected = False
#         # self.connections.pop(port_1)

#     @abstractmethod
#     def create_inputs(self):
#         pass

#     @abstractmethod
#     def create_outputs(self):
#         pass

#     @abstractmethod
#     def node_operation(self):
#         pass
