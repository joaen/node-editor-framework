from PySide2 import QtCore, QtWidgets, QtGui


class GraphicsRect(QtWidgets.QGraphicsItem):

    def __init__(self):
        super().__init__()

        self.outline_color = QtGui.QColor(30, 30, 30)
        self.color = QtGui.QColor(45, 45, 48)

        self.width = 200
        self.height = 200

        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(60)
        self.shadow.setOffset(2, 2)
        self.shadow.setColor(self.outline_color)
        self.setGraphicsEffect(self.shadow)


    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter: QtGui.QPainter, option, widget=None):
        painter.setBrush(QtGui.QBrush(self.color))
        painter.setPen(QtGui.QPen(self.outline_color))
        painter.drawRoundedRect(0, 0, self.boundingRect().width(), self.boundingRect().height(), 15, 15)