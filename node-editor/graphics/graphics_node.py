from functools import partial
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QPen, QColor, QFont
from PySide2.QtWidgets import QGraphicsItem, QLabel, QGraphicsProxyWidget
from graphics.graphics_port import GraphicsPort
from graphics.graphics_rect import GraphicsRect
from graphics.graphics_header import GraphicsHeader
from graphics.port_label_widget import PortLabelWidget


class GraphicsNode(QGraphicsItem):

    def __init__(self, name="Node", header_color=None, default_value=0, id=None):
        super().__init__()
        self.default_value = default_value
        self.id = id
        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)
        name_label = QLabel(name)
        name_label.setStyleSheet("background-color: transparent; color: white;")
        font = QFont()
        font.setPointSize(11)
        name_label.setFont(font)
        name_label_widget = QGraphicsProxyWidget(parent=self)
        name_label_widget.setWidget(name_label)
        name_label_widget.setZValue(self.zValue() + 1)

        self.header_shape = GraphicsHeader(color=QColor(*header_color))
        self.header_shape.setParentItem(self)
        name_label_widget.setPos((self.node_shape.boundingRect().width() / 2) - (name_label.width() / 2), self.header_shape.boundingRect().y() + (self.header_shape.boundingRect().height() / 2) - (name_label.height() / 2))
    
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

    def create_ports(self, ports):
        io_ports = ports
        node_ports = {}
        y_position = 50
        
        for port_name in io_ports.keys():
            if port_name:
                x_position = (lambda: 0 if io_ports.get(port_name).is_input else 100)()
                port_shape = GraphicsPort(parent=self, pos=QPointF(x_position, y_position), is_input=io_ports.get(port_name).is_input)
                port_shape.setParentItem(self)
                port_shape.setZValue(port_shape.zValue() + 1)
                port_label_widget = self._create_port_widget(label_text=port_name, port=port_shape, alignment=(lambda: "left" if io_ports.get(port_name).is_input else "right")())
                port_shape.port_widget = port_label_widget
                self.node_shape.height += 40
                y_position += 35
                node_ports[port_shape] = io_ports.get(port_name)
        return node_ports

            
    def _create_port_widget(self, label_text, port, alignment):
        port_label_widget = PortLabelWidget(label=label_text, alignment=alignment)
        port_label_widget.text_edit.setText(str(self.default_value))
        port_label_proxy = QGraphicsProxyWidget(parent=self)
        port_label_proxy.setWidget(port_label_widget)
        port_label_proxy.setPos(0, (port.port_pos().y() - 15))
        port_label_widget.text_edit.returnPressed.connect(partial(self._text_changed, port))
        port_label_widget.text_edit.editingFinished.connect(partial(self._text_changed, port))    
        return port_label_widget

    def _text_changed(self, port):
        self.scene().port_text_changed_signal.emit(str(self.id), port, port.port_widget.text_edit.text())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().node_moved_signal.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            if self.scene() is not None:
                view = self.scene().views()[0]
                view.centerOn(self)

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
