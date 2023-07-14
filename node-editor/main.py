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
import node.editor as ne
from node.example_node import ExampleNode
from node.float_node import FloatNode
from node.sum_node import SumNode
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
        self.lines = []
        self.first_port_clicked = {}
        self.second_port_clicked = {}

        ##DEBUG
        self.create_example_node()
        self.create_float_node()

    def create_ui_widgets(self):
        self.scene = EditorGraphicsScene()
        self.view = EditorGraphicsView(self.scene)
        self.view.setScene(self.scene)
        self.scene.add_contextmenu_item(self.create_example_node, "Example Node")
        self.scene.add_contextmenu_item(self.create_sum_node, "Sum Node")
        self.scene.add_contextmenu_item(self.create_float_node, "Float Node")

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

    def create_example_node(self):
        logic_node = ExampleNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(0,169,244))
        graphics_node.create_ports(logic_node.input_ports_dict.values(), input=True)
        graphics_node.create_ports(logic_node.output_ports_dict.values(), input=False)
        self.scene.addItem(graphics_node)
        self.nodes.append(graphics_node)

    def create_float_node(self):
        logic_node = FloatNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(255,152,0))
        graphics_node.create_ports(logic_node.input_ports_dict.values(), input=True)
        graphics_node.create_ports(logic_node.output_ports_dict.values(), input=False)
        self.scene.addItem(graphics_node)
        self.nodes.append(graphics_node)

    def create_sum_node(self):
        logic_node = SumNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(140,195,74))
        graphics_node.create_ports(logic_node.input_ports_dict.values(), input=True)
        graphics_node.create_ports(logic_node.output_ports_dict.values(), input=False)
        self.scene.addItem(graphics_node)
        self.nodes.append(graphics_node)

    def create_connections(self):
        self.scene.node_moved_signal.connect(self.update_line)
        self.scene.port_pressed_signal.connect(self.port_pressed)
        self.scene.line_pressed_signal.connect(self.delete_line)

    def port_pressed(self, port_id, graphics_port):
        two_ports_clicked = False
        if self.first_port_clicked and self.second_port_clicked:
            self.first_port_clicked.clear()
            self.second_port_clicked.clear()

        if self.first_port_clicked:
            self.second_port_clicked[port_id] = graphics_port
            two_ports_clicked = True

        elif self.first_port_clicked == {}:
            self.first_port_clicked[port_id] = graphics_port
        
        if two_ports_clicked:
            connection = ne.create_connection(list(self.first_port_clicked.keys())[0], list(self.second_port_clicked.keys())[0])
            if connection:
               self.create_line(list(self.first_port_clicked.values())[0], list(self.second_port_clicked.values())[0], connection=connection)
                

    def create_line(self, port_one : GraphicsPort, port_two : GraphicsPort, connection):
        line = GraphicsLine(port_one=port_one, port_two=port_two, connection_list=connection)
        self.lines.append(line)
        self.scene.addItem(line)
        self.update_line()

    def delete_line(self, connection_list, graphics_line):
        try:
            self.scene.removeItem(graphics_line)
            ne.break_connection(connection_list[0])
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