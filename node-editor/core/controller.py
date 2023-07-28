from core.logic_node import LogicNode
from core.logic_port import LogicPort
from graphics.graphics_node import GraphicsNode

from example_nodes.multiply_node import MultiplyNode # Example node
from example_nodes.float_node import FloatNode # Example node
from example_nodes.add_node import AddNode # Example node

class Controller():

    def __init__(self):
        self.connections = []
        self.nodes = []

    @classmethod
    def create_connection(cls, port_1: LogicPort, port_2: LogicPort):
        if port_1.is_connected and port_2.is_connected:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port_1))
            return None
        if port_2.is_connected and port_2.is_input:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port_1))
            return None
        if port_1.is_connected and port_1.is_input:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port_1))
            return None
        elif port_1 == port_2:
            print("CAN'T CONNECT PORT TO ITSELF")
            return None
        elif port_1.is_input and port_2.is_input:
            print("YOU CAN'T CONNECT TWO INPUT PORTS")
            return None
        elif port_1.is_input == False and port_2.is_input == False:
            print("YOU CAN'T CONNECT TWO OUTPUT PORTS")
            return None
        elif port_1.node == port_2.node:
            print("YOU CAN'T CONNECT NODE TO ITSELF")
            return None
        else:
            port_1.connection = port_2
            port_2.connection = port_1
            port_1.is_connected = True
            port_2.is_connected = True
            print("Connected: {} || {}".format(port_1.node, port_2.node))
            return [port_1, port_2]

    @classmethod
    def break_connection(cls, port_1: LogicPort, port_2: LogicPort):
        port_1.connection = None
        port_2.connection = None
        port_1.is_connected = False
        port_2.is_connected = False
        print("Broke connection between: {} AND {} ".format(port_1, port_2))

    @classmethod
    def delete_node(cls, node : LogicNode):
        node.exsist = False
        print("Deleted node: {}".format(node))

    @classmethod
    def create_node(cls, node_name):
        node_class = globals().get(node_name)

        if node_class and issubclass(node_class, LogicNode):
            logic_node = node_class()
            return logic_node
        else:
            raise ValueError(f"No LogicNode subclass named {node_name} exists in the current namespace")

