from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from graphics.line import GraphicsLine
from graphics.node import GraphicsNode


class EditorGraphicsScene(QGraphicsScene):

    NodeMoved = Signal(QPointF)
    PortPressed = Signal(bool)
    createNewNodeRequested = Signal()

    def __init__(self):
        super().__init__()

        self.nodes = []

        self.background_color = QColor(30, 30, 30)
        self.grid_color = QColor(45, 45, 48)
        self.grid_spacing = 30
        self.pen = QPen(self.grid_color, 1, Qt.DotLine)

        self.setSceneRect(QRectF(-1000, -1000, 2000, 2000))
        self.setBackgroundBrush(self.background_color)
        self.create_node(0)
        self.create_node(1)
        self.create_connections()
        self.initContextMenu()

    def initContextMenu(self):
        self.contextMenu = QMenu()
        self.action1 = QAction("New Node", self)
        self.action1.triggered.connect(self.create_node)
        self.contextMenu.addAction(self.action1)

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

    def create_node(self, pos):
        node = GraphicsNode(name="Node 001", port_pos=pos)
        self.addItem(node)
        self.nodes.append(node)

    def create_connections(self):
        self.NodeMoved.connect(self.updateLine)
        self.PortPressed.connect(self.create_line)
        self.createNewNodeRequested.connect(self.create_node)

    def create_line(self):
        self.line = GraphicsLine(self.nodes[0].port_pos().x(), self.nodes[0].port_pos().y(), self.nodes[1].port_pos().x(), self.nodes[1].port_pos().y())
        self.addItem(self.line)
        self.updateLine()
        

    def updateLine(self):
        try:
            self.line.end_point_x = self.nodes[0].port_pos().x()
            self.line.end_point_y = self.nodes[0].port_pos().y()
            self.line.start_point_x = self.nodes[1].port_pos().x()
            self.line.start_point_y = self.nodes[1].port_pos().y()
        except:
            pass
