from functools import partial
import sys
import traceback
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphics.graphics_scene import EditorGraphicsScene
from graphics.graphics_view import EditorGraphicsView

from graphics.graphics_line import GraphicsLine
from graphics.graphics_node import GraphicsNode
from graphics.graphics_port import GraphicsPort
from graphics.graphics_mouse_line import GraphicsMouseLine
import node.editor as ne
from node.multiply_node import MultiplyNode
from node.float_node import FloatNode
from node.add_node import AddNode
from node.node import Node
from node.port import Port


class MainWindow(QWidget): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Editor")
        self.setBaseSize(QSize(600, 600))
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_connections()
        self.nodes = []
        self.lines: list[GraphicsLine] = []
        self.clicked_ports = []
        self.connections = []
        self.is_following_mouse = False
        self.graphics_mouse_line: GraphicsMouseLine = None

        ##DEBUG
        self.create_sum_node()
        self.create_float_node()
        self.create_multiply_node()
    
    def create_ui_widgets(self):
        self.scene = EditorGraphicsScene()
        self.view = EditorGraphicsView(self.scene)
        self.view.setScene(self.scene)

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

    def create_connections(self):
        self.scene.add_contextmenu_item(self.create_sum_node, "Sum Node")
        self.scene.add_contextmenu_item(self.create_multiply_node, "Multiply Node")
        self.scene.add_contextmenu_item(self.create_float_node, "Float Node")
        self.scene.create_key_event(Qt.Key_Delete, partial(self.delete_object))
        self.scene.mouse_position_signal.connect(self.mouse_moved)
        self.scene.node_moved_signal.connect(self.update_line)
        self.scene.port_pressed_signal.connect(self.port_pressed)
        self.scene.port_text_changed_signal.connect(self.port_text_changed)

    def port_text_changed(self, port: Port, value):
        port.data = value
        self.update_nodes()

    def mouse_moved(self, mouse_pos):
        if self.is_following_mouse == True:
            clicked_one, clicked_one_graphics = self.clicked_ports[0]
            self.graphics_mouse_line.update_pos(pos1=clicked_one_graphics.port_pos(), pos2=mouse_pos)

    def create_multiply_node(self):
        logic_node = MultiplyNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(0,169,244), default_value=logic_node.default_value)
        graphics_node.create_ports(input=logic_node.input_ports_dict, output=logic_node.output_ports_dict)
        self.scene.addItem(graphics_node)
        self.nodes.append((logic_node, graphics_node))

    def create_float_node(self):
        logic_node = FloatNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(255,152,0), default_value=logic_node.default_value)
        graphics_node.create_ports(input=logic_node.input_ports_dict, output=logic_node.output_ports_dict)
        self.scene.addItem(graphics_node)
        self.nodes.append((logic_node, graphics_node))

    def create_sum_node(self):
        logic_node = AddNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(140,195,74), default_value=logic_node.default_value)
        graphics_node.create_ports(input=logic_node.input_ports_dict, output=logic_node.output_ports_dict)
        self.scene.addItem(graphics_node)
        self.nodes.append((logic_node, graphics_node))

    def update_nodes(self):
        for node in self.nodes:
            logic_node: Node
            graphics_node: GraphicsNode
            logic_node, graphics_node = node
            logic_node.update()
        
            for port in graphics_node.ports:
                key, port_shape = port
                if key != "input":
                    port_shape.set_input_text(port_shape.port_id.data)
        
        for connection in self.connections:
            port_1, port_1_shape, port_2, port_2_shape = connection
            if port_1.is_input:
                port_1_shape.set_input_text(port_2_shape.port_id.data)
            if port_2.is_input:
                port_2_shape.set_input_text(port_1_shape.port_id.data)

    def port_pressed(self, port_id, graphics_port):  
        self.clicked_ports.append((port_id, graphics_port))
        
        if len(self.clicked_ports) >= 2:
            self.scene.removeItem(self.graphics_mouse_line)
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            clicked_port_2, clicked_port_2_graphics = self.clicked_ports[1]
            connection = ne.create_connection(clicked_port_1, clicked_port_2)
            if connection:
                self.connections.append((clicked_port_1, clicked_port_1_graphics, clicked_port_2, clicked_port_2_graphics))
                self.create_line(clicked_port_1_graphics, clicked_port_2_graphics)
                self.update_nodes()

            self.is_following_mouse = False
            self.clicked_ports.clear()
        
        if len(self.clicked_ports) == 1:
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            self.graphics_mouse_line = GraphicsMouseLine(point_one=clicked_port_1_graphics.port_pos(), point_two=clicked_port_1_graphics.port_pos())
            self.scene.addItem(self.graphics_mouse_line)
            self.is_following_mouse = True

    def create_line(self, port_one : GraphicsPort, port_two : GraphicsPort):
        line = GraphicsLine(port_one=port_one, port_two=port_two)
        line.setZValue(line.zValue() - 1)
        self.lines.append(line)
        self.scene.addItem(line)
        self.update_line()

    def delete_object(self):
        try:
            for item in self.scene.selectedItems():
                if isinstance(item, GraphicsLine):
                    ne.break_connection(item.port_one.port_id, item.port_two.port_id)
                    self.scene.removeItem(item)
                if isinstance(item, GraphicsNode):
                    ne.delete_node(item)
                    self.scene.removeItem(item)
        except:
            traceback.print_exc()
        
    def update_line(self):
        try:
            for line in self.lines:
                line.update_pos()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()