from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.graphics_port import GraphicsPort
from graphics.graphics_rect import GraphicsRect
from graphics.graphics_header import GraphicsHeader


class GraphicsNode(QGraphicsItem):

    def __init__(self, name="Node", header_color=None):
        super().__init__()

        
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
        # ports
        y_position = 50
        for key, value in kwargs.items():
            for port in value.keys():
                x_position = (lambda: 0 if key == "input" else 100)()
                port_shape = GraphicsPort(port_id=value.get(port), pos=QPointF(x_position, y_position), label=port, is_input=(lambda: True if key == "input" else False)())
                port_shape.setParentItem(self)
                self.node_shape.height += 40
                y_position += 35
                self.ports.append(port_shape)
            # return ports

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
