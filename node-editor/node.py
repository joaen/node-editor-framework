from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from node_port import Port

class Node():
    input_port = Port()
    output_port = Port()

    def __init__(self, scene, title, inputs=[], outputs=[]):

        self.input_port.data = 5
        self.output_port.data = 0
        self.node_operation()

        
    def node_operation(self):
        # Takes input and add 5 to it
        output = (self.input_port.data + 5)
        self.output_port.data = output
