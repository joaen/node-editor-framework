from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class GraphicsCircle(QGraphicsItem):
    def __init__(self, x=200, y=200, radius=20):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius

    def mousePressEvent(self, event):
        print("Circle clicked!")

    def boundingRect(self):
        return QRectF(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def paint(self, painter: QPainter, option, widget):
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QColor(0, 255, 0))
        painter.drawEllipse(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)