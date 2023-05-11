from PySide2.QtCore import *
import PySide2.QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics_circle import GraphicsCircle
from graphics_rect import GraphicsRect
from graphics_line import GraphicsLine


class GraphicsNode(QGraphicsItem):

    def __init__(self):
        super().__init__()
        self.text = QLabel("WIWOWOWOOWOWOWOWWW")        
        self.proxy = QGraphicsProxyWidget(parent=self)
        self.proxy.setWidget(self.text)
        self.proxy.setPos(0, 0)
        self.proxy.setZValue(self.zValue() + 1)

        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)

        self.port_shape = GraphicsCircle()
        self.port_shape.setParentItem(self)
        self.port_shape.setPos(0, 100)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().NodeMoved.emit(self.pos())

    def boundingRect(self):
        return self.port_shape.boundingRect().united(self.node_shape.boundingRect())

    def paint(self, painter, option, widget):
        pass
