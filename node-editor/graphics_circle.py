from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class GraphicsCircle(QGraphicsItem):

    def __init__(self, x=200, y=200, radius=20):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = QColor(255, 165, 0)

    def mousePressEvent(self, event):
        print("PRESSED")
        if event.button() == Qt.LeftButton:
            self.color = QColor(255, 0, 0)
            self.update()
        else:
            return super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.color = QColor(255, 165, 0)
            self.update()
        else:
            return super().mouseReleaseEvent(event)

    def boundingRect(self):
        return QRectF(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def paint(self, painter: QPainter, option, widget):
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(self.color)
        painter.drawEllipse(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)