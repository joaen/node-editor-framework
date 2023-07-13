from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.graphics_port import GraphicsPort


class GraphicsLine(QGraphicsItem):

    def __init__(self, port_one : GraphicsPort, port_two : GraphicsPort):
        super().__init__()
        self.port_one = port_one
        self.port_two = port_two
        self.start_point_x = self.port_one.port_pos().x()
        self.start_point_y = self.port_one.port_pos().y()
        self.end_point_x = self.port_two.port_pos().x()
        self.end_point_y = self.port_two.port_pos().y()
        self.path = QPainterPath()
        self.color = QColor(255, 255, 255)

    # def mousePressEvent(self, event):
    #     print("PRESSED LINE")
    #     super().mousePressEvent(event)

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter: QPainter, option, widget):
        self.path.clear()
        pen = QPen(self.color)
        pen.setWidth(2)
        painter.setPen(pen)

        start_point = QPointF(self.start_point_x, self.start_point_y)
        self.path.moveTo(start_point)

        point1 = QPointF((self.start_point_x + 100), self.start_point_y)
        point2 = QPointF((self.end_point_x - 100), self.end_point_y)
        end_point = QPointF(self.end_point_x, self.end_point_y)
        self.path.cubicTo(point1, point2, end_point)
        painter.drawPath(self.path)

    def update_pos(self):
        self.start_point_x = self.port_one.port_pos().x()
        self.start_point_y = self.port_one.port_pos().y()
        self.end_point_x = self.port_two.port_pos().x()
        self.end_point_y = self.port_two.port_pos().y()
        self.update()