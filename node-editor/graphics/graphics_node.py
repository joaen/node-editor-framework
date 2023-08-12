from functools import partial
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QPen, QColor
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

        name_label_widget = QGraphicsProxyWidget(parent=self)
        name_label_widget.setWidget(name_label)
        name_label_widget.setPos((self.node_shape.boundingRect().width() / 2) - (name_label.width() / 2), 15)
        name_label_widget.setZValue(self.zValue() + 1)

        self.header_shape = GraphicsHeader(color=QColor(*header_color))
        self.header_shape.setParentItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def create_ports(self, input, output):
        ports = {}
        io_dict = {}
        io_dict.update(input)
        io_dict.update(output)
        y_position = 50
        
        for port_name in io_dict.keys():
            if port_name:
                x_position = (lambda: 0 if io_dict.get(port_name).is_input else 100)()
                port_shape = GraphicsPort(port_id=io_dict.get(port_name), parent=self, pos=QPointF(x_position, y_position), is_input=io_dict.get(port_name).is_input)
                port_shape.setParentItem(self)
                port_shape.setZValue(port_shape.zValue() + 1)
                port_label_widget = self._create_port_widget(label_text=port_name, port=port_shape, alignment=(lambda: "left" if io_dict.get(port_name).is_input else "right")())
                port_shape.port_widget = port_label_widget
                self.node_shape.height += 40
                y_position += 35
                ports[port_shape] = io_dict.get(port_name)
        return ports

            
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

    # @classmethod
    # def create_ui_node(cls, logic_node, scene):
    #     graphics_node = GraphicsNode(name=logic_node.NAME, header_color=logic_node.node_color, default_value=logic_node.default_value)
    #     graphics_node.create_ports(input=logic_node.input_ports, output=logic_node.output_ports)
    #     scene.addItem(graphics_node)
    #     return graphics_node
