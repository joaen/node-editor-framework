from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.graphics_port import GraphicsPort
from graphics.graphics_rect import GraphicsRect
from graphics.graphics_header import GraphicsHeader
from node.node import Node


class GraphicsNode(QGraphicsItem):

    def __init__(self, name="Node", header_color=None):
        super().__init__()
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("background-color: transparent; color: white;")
        self.proxy = QGraphicsProxyWidget(parent=self)
        self.proxy.setWidget(self.name_label)
        self.proxy.setPos(70, 15)
        self.proxy.setZValue(self.zValue() + 1)
        
        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)
        # self.node_shape.setFlag(QGraphicsItem.ItemIsSelectable)

        self.header_shape = GraphicsHeader(color=header_color)
        self.header_shape.setParentItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def create_ports(self, ports=None, input=False):
        y_position = 50
        if input == True:
            for port in ports:
                self.port_shape = GraphicsPort(port_id=port, is_input=True)
                self.port_shape.setPos(QPointF(0, y_position))
                self.port_shape.x = 0
                self.port_shape.y = y_position
                self.port_shape.setParentItem(self)
                y_position += 50
        
        if input == False:
            for port in ports:
                self.port_shape = GraphicsPort(port_id=port, is_input=False)
                self.port_shape.setPos(QPointF(100, 50))
                self.port_shape.x = 100
                self.port_shape.y = 50
                self.port_shape.setParentItem(self)
                y_position += 50
    

    def port_pos(self):
        return self.port_shape.mapToScene(self.port_shape.pos())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().node_moved_signal.emit()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            if value:
                self.scene().node_pressed_signal.emit(self)
        return super().itemChange(change, value)

    def boundingRect(self):
        return self.node_shape.boundingRect()

    def paint(self, painter, option, widget):
        # pass
        if self.isSelected():
            painter.setPen(QPen(QColor(255, 255, 255), 5, Qt.SolidLine))
            painter.drawRoundedRect(0, 0, 200, 300, 15, 15)
