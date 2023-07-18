from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.graphics_port import GraphicsPort
from graphics.graphics_rect import GraphicsRect
from graphics.graphics_header import GraphicsHeader
from node.node import Node
from graphics.port_label_widget import PortLabelWidget


class GraphicsNode(QGraphicsItem):

    def __init__(self, name="Node", header_color=None):
        super().__init__()

        
        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)

        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("background-color: transparent; color: white;")

        self.name_label_widget = QGraphicsProxyWidget(parent=self)
        self.name_label_widget.setWidget(self.name_label)
        self.name_label_widget.setPos((self.node_shape.boundingRect().width() / 2) - (self.name_label.width() / 2), 15)
        self.name_label_widget.setZValue(self.zValue() + 1)

        self.header_shape = GraphicsHeader(color=header_color)
        self.header_shape.setParentItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def create_ports(self, **kwargs):
        y_position = 50
        for key, value in kwargs.items():
            for port in value.keys():
                x_position = (lambda: 0 if key == "input" else 100)()
                self.port_shape = GraphicsPort(port_id=value.get(port))
                self.port_shape.setPos(QPointF(x_position, y_position))
                self.port_shape.x = x_position
                self.port_shape.y = y_position
                self.port_shape.setParentItem(self)

                port_label_widget = PortLabelWidget(label=port, alignment=(lambda: "left" if key == "input" else "right")())
                port_label_proxy = QGraphicsProxyWidget(parent=self)
                port_label_proxy.setWidget(port_label_widget)
                port_label_proxy.setZValue(self.zValue() + 1)
                port_label_proxy.setPos(0, (self.port_shape.port_pos().y() - 15))
                print(input)
                print(y_position)
                y_position += 35
            print("--")


            # Try to add a vlue 
            # Add the value box position at the name_label + the name_label x value (width)
            # value_box_pos_x = (lambda: True if input else False)()
            # label_width = (lambda: label_pos_x + name_label.width() if input else (name_label.width() * -1) + label_pos_x)()
            # value_box = QLineEdit()
            # value_box.setFixedWidth(40)
            # value_box_pos = (label_pos_x + -label_pos_x) - name_label.width()
            # # name_label.setStyleSheet("background-color: transparent; color: white; text-align: right;")
            # value_box_proxy = QGraphicsProxyWidget(parent=self)
            # value_box_proxy.setWidget(value_box)
            # value_box_proxy.setPos(value_box_pos, self.port_shape.port_pos().y() - 11)
            

    def port_pos(self):
        return self.port_shape.mapToScene(self.port_shape.pos())

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
            painter.drawRoundedRect(0, 0, 200, 300, 15, 15)
