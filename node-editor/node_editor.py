
from node.port import Port

def create_connection(port_1: Port, port_2: Port):
    if port_1.is_connected:
        print("THIS PORT IS ALREADY CONNECTED")
    else:
        port_1.connection = port_2
        port_2.connection = port_1
        port_1.is_connected = True
        port_2.is_connected = True
        print("Connected: {} || {}".format(port_1.node, port_2.node))

def break_connection(port_1: Port):
    port_2 = port_1.connection
    port_1.connection = None
    port_2.connection = None
    port_1.is_connected = False
    port_2.is_connected = False