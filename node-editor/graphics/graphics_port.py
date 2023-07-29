from PySide2 import QtCore, QtWidgets, QtGui
from graphics.port_label_widget import PortLabelWidget


class GraphicsPort(QtWidgets.QGraphicsItem):

    def __init__(self, port_id, is_input, pos: QtCore.QPointF, parent):
        super().__init__()
        self.parent_node = parent
        self.setPos(pos)
        self.port_id = port_id
        self.is_input = is_input
        self.port_widget: PortLabelWidget
        self.radius = 10
        self.color = QtGui.QColor(255, 255, 255)
        self.click_color = QtGui.QColor(0, 255, 0)
        self.border_color = QtGui.QColor(255, 255, 255)
        self.hover_color = QtGui.QColor(155, 155, 155)
        self.diameter = max(self.boundingRect().width(), self.boundingRect().height())

        self.pen = QtGui.QPen(self.color)
        self.pen.setWidth(1)
        self.brush = QtGui.QBrush(self.color)
        self.setAcceptHoverEvents(True)

    def set_input_text(self, text):
        self.port_widget.text_edit.setText(str(text))
        self.input_text = text

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.scene().port_pressed_signal.emit(self.port_id, self)
            self.brush.setColor(self.click_color)
            self.update()
        else:
            return super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.brush.setColor(self.color)
            self.update()
        else:
            return super().mouseReleaseEvent(event)
        
    def hoverEnterEvent(self, event):
        self.brush.setColor(self.hover_color)
        self.update()
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.brush.setColor(self.color)
        self.update()
        return super().hoverLeaveEvent(event)

    def boundingRect(self):
        return QtCore.QRectF(self.pos().x() - self.radius, self.pos().y() - self.radius, self.radius * 2, self.radius * 2)
    
    def port_pos(self):
        return self.mapToScene(self.pos())

    def paint(self, painter: QtGui.QPainter, option, widget):
        painter.setBrush(self.brush)
        painter.drawEllipse(self.boundingRect())