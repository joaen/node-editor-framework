from PySide2 import QtCore, QtGui, QtWidgets

class GraphicsHeader(QtWidgets.QGraphicsItem):

    def __init__(self, color):
        super().__init__()
        self.outline_color = color
        self.color = color

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 200, 40)
    
    def paint(self, painter: QtGui.QPainter, option, widget=None):
        painter.setBrush(QtGui.QBrush(self.color))
        painter.setPen(QtGui.QPen(self.outline_color))
        painter.drawRoundedRect(0, 0, 200, 40, 15, 15)
        painter.drawRect(0, 20, 200, 20)