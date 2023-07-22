from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.port_label_widget import PortLabelWidget



class GraphicsPort(QGraphicsItem):

    def __init__(self, port_id, is_input, label, pos: QPointF):
        super().__init__()
        self.setPos(pos)
        self.port_id = port_id
        self.is_input = is_input
        self.port_widget: PortLabelWidget
        # self.input_text = 0
        self.radius = 8
        self.color = QColor(255, 255, 255)
        self.click_color = QColor(255, 0, 0)
        self.border_color = QColor(255, 255, 255)
        self.diameter = max(self.boundingRect().width(), self.boundingRect().height())

        self.pen = QPen(self.color)
        self.pen.setWidth(2)
        self.brush = QBrush(self.color)
        self.create_port_widget(label)
        self.port_widget.text_edit.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.scene().port_text_changed_signal.emit(self.port_id, self.port_widget.text_edit.text())
        
    def create_port_widget(self, label_text):
        port_label_widget = PortLabelWidget(label=label_text, alignment=(lambda: "left" if self.is_input == True else "right")())
        port_label_proxy = QGraphicsProxyWidget(parent=self)
        port_label_proxy.setWidget(port_label_widget)
        port_pos_x = (lambda: self.pos().x() if self.is_input == True else (self.pos().x() - port_label_widget.width()))()
        port_label_proxy.setPos(port_pos_x, (self.pos().y() - 15))
        self.port_widget = port_label_widget
        # self.input_text = self.port_widget.text_edit.text()

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

    def boundingRect(self):
        return QRectF(self.pos().x() - self.radius, self.pos().y() - self.radius, self.radius * 2, self.radius * 2)
    
    def port_pos(self):
        return self.mapToScene(self.pos())

    def paint(self, painter: QPainter, option, widget):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawEllipse(self.pos().x() - self.radius, self.pos().y() - self.radius, self.radius * 2, self.radius * 2)