from functools import partial
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.graphics_port import GraphicsPort
from graphics.graphics_rect import GraphicsRect
from graphics.graphics_header import GraphicsHeader
from graphics.port_label_widget import PortLabelWidget


class GraphicsNode(QGraphicsItem):

    def __init__(self, name="Node", header_color=None, default_value=0):
        super().__init__()
        self.default_value = default_value
        self.ports = []
        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)
        name_label = QLabel(name)
        name_label.setStyleSheet("background-color: transparent; color: white;")

        name_label_widget = QGraphicsProxyWidget(parent=self)
        name_label_widget.setWidget(name_label)
        name_label_widget.setPos((self.node_shape.boundingRect().width() / 2) - (name_label.width() / 2), 15)
        name_label_widget.setZValue(self.zValue() + 1)

        self.header_shape = GraphicsHeader(color=header_color)
        self.header_shape.setParentItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def create_ports(self, **kwargs):
        y_position = 50
        for key, value in kwargs.items():
            for port in value.keys():
                x_position = (lambda: 0 if key == "input" else 100)()
                port_shape = GraphicsPort(port_id=value.get(port), parent=self, pos=QPointF(x_position, y_position), is_input=(lambda: True if key == "input" else False)())
                port_shape.setParentItem(self)
                port_shape.setZValue(port_shape.zValue() + 1)
                port_label_widget = self.create_port_widget(label_text=port, port=port_shape, alignment=(lambda: "left" if key == "input" else "right")())
                port_shape.port_widget = port_label_widget
                self.node_shape.height += 40
                y_position += 35
                self.ports.append((key, port_shape))
            
    def create_port_widget(self, label_text, port, alignment):
        port_label_widget = PortLabelWidget(label=label_text, alignment=alignment)
        port_label_widget.text_edit.setText(str(self.default_value))
        port_label_proxy = QGraphicsProxyWidget(parent=self)
        port_label_proxy.setWidget(port_label_widget)
        port_label_proxy.setPos(0, (port.port_pos().y() - 15))
        port_label_widget.text_edit.textChanged.connect(partial(self.text_changed, port.port_id))
        return port_label_widget

    def text_changed(self, port_id, text):
        self.scene().port_text_changed_signal.emit(port_id, text)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().node_moved_signal.emit()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            if value:
                self.scene().node_pressed_signal.emit(self)
        return super().itemChange(change, value)

    def boundingRect(self):
        return self.node_shape.boundingRect()

    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(QPen(QColor(255, 255, 255), 5, Qt.SolidLine))
            painter.drawRoundedRect(0, 0, self.node_shape.width, self.node_shape.height, 15, 15)
