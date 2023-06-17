from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class GraphicsPort(QGraphicsItem):

    def __init__(self, logic_port):
        super().__init__()
        self.logic_port = logic_port
        self.x = 0
        self.y = 0
        self.radius = 5
        self.color = QColor(255, 255, 255)
        self.click_color = QColor(255, 0, 0)
        self.border_color = QColor(255, 255, 255)

        self.pen = QPen(self.color)
        self.pen.setWidth(2)
        self.brush = QBrush(self.color)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:

            self.scene().port_pressed_signal.emit(self.logic_port)
            print("PRESSED")
            print(self.logic_port)

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