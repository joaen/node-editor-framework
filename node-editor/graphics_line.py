from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics_node import GraphicsNode


class GraphicsLine(QGraphicsItem):

    def __init__(self, node : GraphicsNode):
        super().__init__()
        self.node = node
        self.start_point_x = 0
        self.start_point_y = 0
        self.end_point_x = node.port_pos().x()
        self.end_point_y = node.port_pos().y()

        self.path = QPainterPath()
        self.color = QColor(255, 165, 0)

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter: QPainter, option, widget):


        self.path.clear()
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(5)
        painter.setPen(pen)

        self.path.moveTo(self.start_point_x, self.start_point_y)
        self.path.lineTo(self.end_point_x, self.end_point_y)

        painter.drawPath(self.path)
        
        self.end_point_x = self.node.port_pos().x()
        self.end_point_y = self.node.port_pos().y()