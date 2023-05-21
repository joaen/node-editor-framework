from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Port():

    def __init__(self, data=None):
        self.is_connected = False
        self.is_input = None
        self.connection = None
        self.type = None
        self._data = data

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data

    
