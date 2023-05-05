from PySide2.QtCore import *
import PySide2.QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics_circle import GraphicsCircle
from graphics_rect import GraphicsRect


class GraphicsNode(QGraphicsItem):

    def __init__(self):
        super().__init__()
        
        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)

        self.port_shape = GraphicsCircle()
        self.port_shape.setParentItem(self)


    def boundingRect(self):
        return self.port_shape.boundingRect().united(self.node_shape.boundingRect())

    def paint(self, painter, option, widget):
        pass
    