from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class GraphicsRect(QGraphicsItem):

    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QRectF(200, 200, 300, 300)
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setBrush(QBrush(Qt.gray))
        painter.setPen(QPen(Qt.black))
        painter.drawRect(200, 200, 300, 300)