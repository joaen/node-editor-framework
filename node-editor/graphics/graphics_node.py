from functools import partial
from PySide2 import QtCore, QtWidgets, QtGui
from graphics.graphics_port import GraphicsPort
from graphics.graphics_rect import GraphicsRect
from graphics.graphics_header import GraphicsHeader
from graphics.port_label_widget import PortLabelWidget


class GraphicsNode(QtWidgets.QGraphicsItem):

    def __init__(self, name="Node", header_color=None, default_value=0):
        super().__init__()
        self.default_value = default_value
        self.ports = {}
        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)
        name_label = QtWidgets.QLabel(name)
        name_label.setStyleSheet("background-color: transparent; color: white;")

        name_label_widget = QtWidgets.QGraphicsProxyWidget(parent=self)
        name_label_widget.setWidget(name_label)
        name_label_widget.setPos((self.node_shape.boundingRect().width() / 2) - (name_label.width() / 2), 15)
        name_label_widget.setZValue(self.zValue() + 1)

        self.header_shape = GraphicsHeader(color=QtGui.QColor(*header_color))
        self.header_shape.setParentItem(self)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

    def _create_ports(self, input, output):
        y_position = 50
        combined_dict = input.copy()
        combined_dict.update(output)
        
        for name in combined_dict.keys():
            if name:
                x_position = (lambda: 0 if combined_dict.get(name).is_input else 100)()
                port_shape = GraphicsPort(port_id=combined_dict.get(name), parent=self, pos=QtCore.QPointF(x_position, y_position), is_input=combined_dict.get(name).is_input)
                port_shape.setParentItem(self)
                port_shape.setZValue(port_shape.zValue() + 1)
                port_label_widget = self._create_port_widget(label_text=name, port=port_shape, alignment=(lambda: "left" if combined_dict.get(name).is_input else "right")())
                port_shape.port_widget = port_label_widget
                self.node_shape.height += 40
                y_position += 35
                self.ports[combined_dict.get(name)] = port_shape

            
    def _create_port_widget(self, label_text, port, alignment):
        port_label_widget = PortLabelWidget(label=label_text, alignment=alignment)
        port_label_widget.text_edit.setText(str(self.default_value))
        port_label_proxy = QtWidgets.QGraphicsProxyWidget(parent=self)
        port_label_proxy.setWidget(port_label_widget)
        port_label_proxy.setPos(0, (port.port_pos().y() - 15))
        port_label_widget.text_edit.textChanged.connect(partial(self._text_changed, port.port_id))
        return port_label_widget

    def _text_changed(self, port_id, text):
        self.scene().port_text_changed_signal.emit(port_id, text)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.scene().node_moved_signal.emit()

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:
            if value:
                self.scene().node_pressed_signal.emit(self)
        return super().itemChange(change, value)

    def boundingRect(self):
        return self.node_shape.boundingRect()

    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 5, QtGui.Qt.SolidLine))
            painter.drawRoundedRect(0, 0, self.node_shape.width, self.node_shape.height, 15, 15)

    @classmethod
    def create_ui_node(cls, logic_node, scene):
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=logic_node.node_color, default_value=logic_node.default_value)
        graphics_node._create_ports(input=logic_node.input_ports, output=logic_node.output_ports)
        scene.addItem(graphics_node)
        return graphics_node
