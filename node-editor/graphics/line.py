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
        self.color = QColor(255, 165, 0)

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter: QPainter, option, widget):
        self.path.clear()
        pen = QPen(QColor(255, 165, 0))
        pen.setWidth(5)
        painter.setPen(pen)

        self.path.moveTo(self.start_point_x, self.start_point_y)
        self.path.lineTo(self.end_point_x, self.end_point_y)
        painter.drawPath(self.path)