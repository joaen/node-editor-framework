from PySide2.QtCore import *
import PySide2.QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics_circle import GraphicsCircle
from graphics_rect import GraphicsRect


class GraphicsNode(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.square = GraphicsRect()
        self.square.setParentItem(self)

        self.circle = GraphicsCircle()
        self.circle.setParentItem(self)


    def boundingRect(self):
        return self.circle.boundingRect().united(self.square.boundingRect())

    def paint(self, painter, option, widget):
        pass
    