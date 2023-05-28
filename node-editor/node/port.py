from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Port():

    def __init__(self, is_input=True, parent_node=None):
        self._data = None
        self.node = parent_node
        self.connection : Port = None
        self.is_connected = False
        self.is_input = is_input

    @property
    def data(self):
        if self.is_input and self.is_connected:
            self._data = self.connection.data
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data

    # @property
    # def connection(self):
    #     return self._connection
    
    # @connection.setter
    # def connection(self, port):
    #     self._connection = port

    
