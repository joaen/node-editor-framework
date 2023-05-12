from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class GraphicsLine(QGraphicsItem):

    def __init__(self, start_point_x, start_point_y, end_point_x, end_point_y):
        super().__init__()
        self.start_point_x = start_point_x
        self.start_point_y = start_point_y
        self.end_point_x = end_point_x
        self.end_point_y = end_point_y

        self.path = QPainterPath()
        self.color = QColor(255, 255, 255)

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