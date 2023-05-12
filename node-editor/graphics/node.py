from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.circle import GraphicsCircle
from graphics.rect import GraphicsRect
from graphics.header import GraphicsHeader


class GraphicsNode(QGraphicsItem):

    def __init__(self, name="Node", port_pos=int, header_color=None):
        super().__init__()
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("background-color: transparent; color: white;")
        self.proxy = QGraphicsProxyWidget(parent=self)
        self.proxy.setWidget(self.name_label)
        self.proxy.setPos(70, 15)
        self.proxy.setZValue(self.zValue() + 1)

        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)

        self.header_shape = GraphicsHeader(color=header_color)
        self.header_shape.setParentItem(self)

        # Set port position
        self.port_shape = GraphicsCircle()
        if port_pos == 0:
            self.port_shape.setPos(QPointF(0, 50))
            self.port_shape.x = 0
            self.port_shape.y = 50
        if port_pos == 1:
            self.port_shape.setPos(QPointF(100, 50))
            self.port_shape.x = 100
            self.port_shape.y = 50
        self.port_shape.setParentItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def port_pos(self):
        return self.port_shape.mapToScene(self.port_shape.pos())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().NodeMoved.emit()

    def boundingRect(self):
        return self.port_shape.boundingRect().united(self.node_shape.boundingRect())

    def paint(self, painter, option, widget):
        pass
