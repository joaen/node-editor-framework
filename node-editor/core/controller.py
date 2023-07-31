from core.logic_node import LogicNode
from core.logic_port import LogicPort

from example_nodes.multiply_node import MultiplyNode # Example node
from example_nodes.float_node import FloatNode # Example node
from example_nodes.add_node import AddNode # Example node

class Controller():

    def __init__(self):
        self.connections = []
        self.nodes = {}

    def create_connection(self, port1: LogicPort, port2: LogicPort):
        if port1.is_connected and port2.is_connected:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port1))
            return False
        if port2.is_connected and port2.is_input:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port1))
            return False
        if port1.is_connected and port1.is_input:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port1))
            return False
        elif port1 == port2:
            print("CAN'T CONNECT PORT TO ITSELF")
            return False
        elif port1.is_input and port2.is_input:
            print("YOU CAN'T CONNECT TWO INPUT PORTS")
            return False
        elif port1.is_input == False and port2.is_input == False:
            print("YOU CAN'T CONNECT TWO OUTPUT PORTS")
            return False
        elif port1.parent_node == port2.parent_node:
            print("YOU CAN'T CONNECT NODE TO ITSELF")
            return False
        else:
            port1.connection = port2
            port2.connection = port1
            port1.is_connected = True
            port2.is_connected = True
            print("Connected: {} || {}".format(port1.parent_node, port2.parent_node))
            self.connections.append((port1, self.get_ui_node(port1), port2, self.get_ui_node(port2)))
            return True

    def get_ui_node(self, port: LogicPort):
        for ui_node in self.nodes.values():
            for logic_port, ui_port in ui_node.ports.items():
                if logic_port == port:
                    return ui_port
                else: 
                    return None

    def break_connection(self, port_1: LogicPort, port_2: LogicPort):
        port_1.connection = None
        port_2.connection = None
        port_1.is_connected = False
        port_2.is_connected = False

        ports_to_check = {port_1, port_2}
        self.connections = [connection for connection in self.connections if not ports_to_check.issubset(set(connection))]
        print("Broke connection between: {} AND {} ".format(port_1, port_2))
        print(len(self.connections))

    def delete_node(self, node : LogicNode):
        node.exsist = False
        self.nodes.pop(node)
        print("Deleted node: {}".format(node))

    def create_node(self, node_name):
        node_class = globals().get(node_name)

        if node_class and issubclass(node_class, LogicNode):
            logic_node = node_class()
            self.nodes[logic_node] = None
            return logic_node
        else:
            raise ValueError(f"No LogicNode subclass named {node_name} exists in the current namespace")

