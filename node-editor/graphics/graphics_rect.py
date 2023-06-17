from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class GraphicsRect(QGraphicsItem):

    def __init__(self):
        super().__init__()

        self.outline_color = QColor(30, 30, 30)
        self.color = QColor(45, 45, 48)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(60)
        self.shadow.setOffset(2, 2)
        self.shadow.setColor(self.outline_color)
        self.setGraphicsEffect(self.shadow)


    def boundingRect(self):
        return QRectF(0, 0, 200, 300)
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(self.outline_color))
        painter.drawRoundedRect(0, 0, 200, 300, 15, 15)