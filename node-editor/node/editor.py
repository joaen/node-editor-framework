import traceback
from node.node import Node
from node.port import Port

def create_connection(port_1: Port, port_2: Port):
    try:
        if port_1.is_connected:
            print("THIS PORT IS ALREADY CONNECTED".format(port_1))
            return False
        elif port_2.is_connected:
            print("THIS PORT IS ALREADY CONNECTED".format(port_2))
            return False
        elif port_1 == port_2:
            print("CAN'T CONNECT PORT TO ITSELF")
            return False
        elif port_1.is_input and port_2.is_input:
            print("YOU CAN'T CONNECT TWO INPUT PORTS")
            return False
        elif port_1.is_input == False and port_2.is_input == False:
            print("YOU CAN'T CONNECT TWO OUTPUT PORTS")
            return False
        else:
            port_1.connection = port_2
            port_2.connection = port_1
            port_1.is_connected = True
            port_2.is_connected = True
            print("Connected: {} || {}".format(port_1.node, port_2.node))
            return True
    except:
        traceback.print_exc()
        return False
        

def break_connection(port_1: Port):
    port_2 = port_1.connection
    port_1.connection = None
    port_2.connection = None
    port_1.is_connected = False
    port_2.is_connected = False

def delete_node(node : Node):
    node.exsist = False