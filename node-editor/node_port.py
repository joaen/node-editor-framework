from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Port():
    is_connected = False
    connection = None
    data = None

    def __init__(self):
        self.data = "pop"
    
    # def something(self):
        # pass
