from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from node.port import Port

class Node():

    def __init__(self, name, inputs: dict[str, type], outputs: dict[str, type]):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

        self.input_ports = self.create_ports(inputs, input=True)
        self.output_ports = self.create_ports(outputs, input=False)

    def create_ports(self, settings: dict[str, type], input=True):
        ports_dict = {}
        for key in settings.keys():
            ports_dict[key] = Port()
    
        return ports_dict

    # def input_data(self, key):
    #     return self.inputs.get(key)
    
    # def output_data(self, key):
    #     return self.outputs.get(key)

