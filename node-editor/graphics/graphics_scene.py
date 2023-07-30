from PySide2 import QtCore, QtWidgets, QtGui
from graphics.graphics_line import GraphicsLine
from graphics.graphics_port import GraphicsPort
from graphics.graphics_node import GraphicsNode
from core.logic_port import LogicPort


class EditorGraphicsScene(QtWidgets.QGraphicsScene):

    node_moved_signal = QtCore.Signal()
    mouse_position_signal = QtCore.Signal(QtCore.QPointF)
    port_pressed_signal = QtCore.Signal(LogicPort, GraphicsPort)
    line_pressed_signal = QtCore.Signal(GraphicsLine)
    node_pressed_signal = QtCore.Signal(GraphicsNode)
    port_text_changed_signal = QtCore.Signal(LogicPort, str)
    clicked_view_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.contextMenu = QtWidgets.QMenu()
        self.background_color = QtGui.QColor(30, 30, 30)
        self.grid_color = QtGui.QColor(45, 45, 48)
        self.grid_spacing = 30
        self.pen = QtGui.QPen(self.grid_color, 1, QtGui.Qt.DotLine)

        self.key_events = {}

        self.setSceneRect(QtCore.QRectF(-1000, -1000, 2000, 2000))
        self.setBackgroundBrush(self.background_color)

    def create_key_event(self, key : QtCore.Qt.Key, command):
        self.key_events[key] = command

    def keyPressEvent(self, event: QtGui.QKeyEvent):
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
        action = QtWidgets.QAction(name, self)
        action.triggered.connect(command)
        self.contextMenu.addAction(action)
        return action

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