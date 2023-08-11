from PySide2.QtCore import Qt, QPointF, QRectF
from PySide2.QtGui import QPen, QColor, QBrush, QPainter, QMouseEvent
from PySide2.QtWidgets import QGraphicsItem
from graphics.port_label_widget import PortLabelWidget


class GraphicsPort(QGraphicsItem):

    def __init__(self, port_id, is_input: bool, pos: QPointF, parent_node):
        super().__init__()
        self.parent_node = parent_node
        self.setPos(pos)
        self.port_id = port_id
        self.is_input = is_input
        self.port_widget: PortLabelWidget
        self.radius = 10
        self.color = QColor(255, 255, 255)
        self.click_color = QColor(0, 255, 0)
        self.border_color = QColor(255, 255, 255)
        self.hover_color = QColor(155, 155, 155)
        self.diameter = max(self.boundingRect().width(), self.boundingRect().height())

        self.pen = QPen(self.color)
        self.pen.setWidth(1)
        self.brush = QBrush(self.color)
        self.setAcceptHoverEvents(True)

    def set_input_text(self, text):
        self.port_widget.text_edit.setText(str(text))
        self.input_text = text

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scene().port_pressed_signal.emit(self.port_id, self)
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
        
    def hoverEnterEvent(self, event):
        self.brush.setColor(self.hover_color)
        self.update()
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.brush.setColor(self.color)
        self.update()
        return super().hoverLeaveEvent(event)

    def boundingRect(self):
        return QRectF(self.pos().x() - self.radius, self.pos().y() - self.radius, self.radius * 2, self.radius * 2)
    
    def port_pos(self):
        return self.mapToScene(self.pos())

    def paint(self, painter: QPainter, option, widget):
        painter.setBrush(self.brush)
        painter.drawEllipse(self.boundingRect())