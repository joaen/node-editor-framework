from functools import partial
import traceback
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from graphics.graphics_line import GraphicsLine
from graphics.graphics_port import GraphicsPort
from graphics.graphics_node import GraphicsNode
from node.port import Port

class EditorGraphicsScene(QGraphicsScene):

    node_moved_signal = Signal()
    mouse_position_signal = Signal(QPointF)
    port_pressed_signal = Signal(Port, GraphicsPort)
    line_pressed_signal = Signal(GraphicsLine)
    node_pressed_signal = Signal(GraphicsNode)
    port_text_changed_signal = Signal(Port, GraphicsPort)

    def __init__(self):
        super().__init__()

        self.contextMenu = QMenu()
        self.background_color = QColor(30, 30, 30)
        self.grid_color = QColor(45, 45, 48)
        self.grid_spacing = 30
        self.pen = QPen(self.grid_color, 1, Qt.DotLine)

        self.key_events = {}

        self.setSceneRect(QRectF(-1000, -1000, 2000, 2000))
        self.setBackgroundBrush(self.background_color)

    def create_key_event(self, key : Qt.Key, command):
        self.key_events[key] = command

    def keyPressEvent(self, event: QKeyEvent):
        for key in self.key_events.keys():
            if event.key() == key:
                command = self.key_events.get(key)
                command()
            else:
                super().keyPressEvent(event)

    def mouseMoveEvent(self, event):
        mouse_position = event.scenePos()
        self.mouse_position_signal.emit(mouse_position)
        super().mouseMoveEvent(event)

    def add_contextmenu_item(self, command, name):
        self.new_example_node_action = QAction(name, self)
        self.new_example_node_action.triggered.connect(command)
        self.contextMenu.addAction(self.new_example_node_action)

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