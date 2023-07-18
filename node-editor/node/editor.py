import traceback
from node.node import Node
from node.port import Port

def create_connection(port_1: Port, port_2: Port):
    try:
        if port_1.is_connected and port_2.is_connected:
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
        

def break_connection(port_1: Port, port_2: Port):
    port_1.connection = None
    port_2.connection = None
    port_1.is_connected = False
    port_2.is_connected = False
    print("Broke connection between: {} AND {} ".format(port_1, port_2))

def delete_node(node : Node):
    node.exsist = False