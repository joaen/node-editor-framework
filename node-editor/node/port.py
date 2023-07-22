from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Port():

    def __init__(self, is_input=True, parent_node=None):
        self._data = 0
        self.node = parent_node
        self.connection : Port = None
        self.is_connected = False
        self.is_input = is_input

    def set_data(self, data):
        self.data = data

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value


    
