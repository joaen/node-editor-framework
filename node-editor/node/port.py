from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Port():

    def __init__(self, data=None, is_input=True, node=None):
        self.node = node
        self.is_connected = False
        self.is_input = None
        self.type = None
        self._data = data
        self._connection = None

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data

    @property
    def connection(self):
        return self._connection
    
    @connection.setter
    def connection(self, port):
        self._connection = port

    
