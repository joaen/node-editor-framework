from functools import partial
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from graphics.graphics_line import GraphicsLine
from graphics.graphics_node import GraphicsNode
from graphics.graphics_port import GraphicsPort
import node.editor as ne
from node.example_node import ExampleNode
from node.float_node import FloatNode
from node.sum_node import SumNode
from node.port import Port

class EditorGraphicsScene(QGraphicsScene):

    node_moved_signal = Signal()
    port_pressed_signal = Signal(Port, GraphicsPort)
    line_pressed_signal = Signal()

    def __init__(self):
        super().__init__()

        self.port_click = 0
        self.first_port_clicked = {}
        self.second_port_clicked = {}
        self.nodes = []

        self.background_color = QColor(30, 30, 30)
        self.grid_color = QColor(45, 45, 48)
        self.grid_spacing = 30
        self.pen = QPen(self.grid_color, 1, Qt.DotLine)

        self.setSceneRect(QRectF(-1000, -1000, 2000, 2000))
        self.setBackgroundBrush(self.background_color)
        self.create_connections()
        self.initContextMenu()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Backspace:
            self.delete_line()
        else:
            super().keyPressEvent(event)

    def initContextMenu(self):
        self.contextMenu = QMenu()

        self.new_example_node_action = QAction("New Exmaple Node", self)
        self.new_example_node_action.triggered.connect(self.create_example_node)
        self.contextMenu.addAction(self.new_example_node_action)

        self.new_float_node_action = QAction("New Float Node", self)
        self.new_float_node_action.triggered.connect(self.create_float_node)
        self.contextMenu.addAction(self.new_float_node_action)

        self.new_float_node_action = QAction("New Sum Node", self)
        self.new_float_node_action.triggered.connect(self.create_sum_node)
        self.contextMenu.addAction(self.new_float_node_action)

    def contextMenuEvent(self, event):
        self.contextMenu.exec_(event.screenPos())

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(rect.left()) - (int(rect.left()) % self.grid_spacing)
        top = int(rect.top()) - (int(rect.top()) % self.grid_spacing)
        right = int(rect.right())
        bottom = int(rect.bottom())

        for y in range(top, bottom, self.grid_spacing):
            painter.setPen(self.pen)
            painter.drawLine(left, y, right, y)

        for x in range(left, right, self.grid_spacing):
            painter.setPen(self.pen)
            painter.drawLine(x, top, x, bottom)

    def create_example_node(self):
        logic_node = ExampleNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(0,169,244))
        graphics_node.create_ports(logic_node.input_ports_dict.values(), input=True)
        graphics_node.create_ports(logic_node.output_ports_dict.values(), input=False)
        self.addItem(graphics_node)
        self.nodes.append(graphics_node)

    def create_float_node(self):
        logic_node = FloatNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(255,152,0))
        graphics_node.create_ports(logic_node.input_ports_dict.values(), input=True)
        graphics_node.create_ports(logic_node.output_ports_dict.values(), input=False)
        self.addItem(graphics_node)
        self.nodes.append(graphics_node)

    def create_sum_node(self):
        logic_node = SumNode()
        graphics_node = GraphicsNode(name=logic_node.NAME, header_color=QColor(140,195,74))
        graphics_node.create_ports(logic_node.input_ports_dict.values(), input=True)
        graphics_node.create_ports(logic_node.output_ports_dict.values(), input=False)
        self.addItem(graphics_node)
        self.nodes.append(graphics_node)

    def create_connections(self):
        self.node_moved_signal.connect(self.updateLine)
        self.port_pressed_signal.connect(self.port_pressed)
        self.line_pressed_signal.connect(self.delete_line)

    def port_pressed(self, port_id, graphics_port):
        two_ports_clicked = False
        if self.first_port_clicked and self.second_port_clicked:
            print("clear")
            self.first_port_clicked.clear()
            self.second_port_clicked.clear()
        if self.first_port_clicked:
            print("add second")
            self.second_port_clicked[port_id] = graphics_port
            two_ports_clicked = True
        elif self.first_port_clicked == {}:
            print("add first")
            self.first_port_clicked[port_id] = graphics_port
        
        if two_ports_clicked:
            ne.create_connection(list(self.first_port_clicked.keys())[0], list(self.second_port_clicked.keys())[0])
            if list(self.first_port_clicked.keys())[0].is_connected and list(self.second_port_clicked.keys())[0].is_connected:
                self.create_line(list(self.first_port_clicked.values())[0], list(self.second_port_clicked.values())[0])
                

    def create_line(self, port_one : GraphicsPort, port_two : GraphicsPort):
        # print(port_one.port_pos())
        self.line = GraphicsLine(port_one.port_pos().x(), port_one.port_pos().y(), port_two.port_pos().x(), port_two.port_pos().y())
        self.addItem(self.line)
        self.updateLine()
        ## test render lines first
        # self.line.setZValue(self.nodes[0].zValue() - 1)
        # self.line.setStackingOrder(self.nodes[0].stackBefore())

    def delete_line(self):
        self.removeItem(self.line)
        
    def updateLine(self):
        pass
        # try:
        #     self.line.end_point_x = self.nodes[0].port_pos().x()
        #     self.line.end_point_y = self.nodes[0].port_pos().y()
        #     self.line.start_point_x = self.nodes[1].port_pos().x()
        #     self.line.start_point_y = self.nodes[1].port_pos().y()
        # except:
        #     pass
