from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class QEditorGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__()
        self.graphics_scene = scene

        # self.create_ui()
        self.setScene(self.graphics_scene)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
    # def create_ui(self):
        # self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)