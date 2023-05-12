from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class GraphicsCircle(QGraphicsItem):

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.radius = 10
        self.color = QColor(255, 255, 255)
        self.click_color = QColor(255, 0, 0)
        self.border_color = QColor(255, 255, 255)

        self.pen = QPen(self.color)
        self.pen.setWidth(2)
        self.brush = QBrush(self.color)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("PRESSED")
            self.scene().PortPressed.emit()
            self.brush.setColor(self.click_color)
            self.update()
        else:
            return super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.brush.setColor(self.color)
            self.update()
        else:
            return super().mouseReleaseEvent(event)

    def boundingRect(self):
        return QRectF(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def paint(self, painter: QPainter, option, widget):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)