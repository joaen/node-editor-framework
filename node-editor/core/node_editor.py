import traceback
from core.logic_node import LogicNode
from core.logic_port import LogicPort
from graphics.graphics_node import GraphicsNode

from example_nodes.multiply_node import MultiplyNode # Example node
from example_nodes.float_node import FloatNode # Example node
from example_nodes.add_node import AddNode # Example node

def create_connection(port_1: LogicPort, port_2: LogicPort):
    try:
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
    except:
        traceback.print_exc()
        return None

def break_connection(port_1: LogicPort, port_2: LogicPort):
    port_1.connection = None
    port_2.connection = None
    port_1.is_connected = False
    port_2.is_connected = False
    print("Broke connection between: {} AND {} ".format(port_1, port_2))

def delete_node(node : LogicNode):
    node.exsist = False
    print("Deleted node: {}".format(node))

def create_node(node_name):
    node_class = globals().get(node_name)

    if node_class and issubclass(node_class, LogicNode):
        logic_node = node_class()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=logic_node.node_color, default_value=logic_node.default_value)
        graphics_node.create_ports(input=logic_node.input_ports_dict, output=logic_node.output_ports_dict)
        return logic_node, graphics_node
    else:
        raise ValueError(f"No LogicNode subclass named {node_name} exists in the current namespace")

