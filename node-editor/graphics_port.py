from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class GraphicsPort(QGraphicsItem):
    def __init__(self, x=200, y=200, radius=20):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawEllipse(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)