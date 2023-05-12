from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class GraphicsHeader(QGraphicsItem):

    def __init__(self, color):
        super().__init__()
        self.outline_color = color
        self.color = color


    def boundingRect(self):
        return QRectF(0, 0, 200, 40)
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(self.outline_color))
        painter.drawRoundedRect(0, 0, 200, 40, 15, 15)
        painter.drawRect(0, 20, 200, 20)