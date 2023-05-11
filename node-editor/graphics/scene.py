from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from graphics.line import GraphicsLine
from graphics.node import GraphicsNode


class EditorGraphicsScene(QGraphicsScene):

    NodeMoved = Signal(QPointF)

    def __init__(self):
        super().__init__()

        self.bg_color = QColor(90, 90, 90)
        self.grid_color = QColor(150, 150, 150)
        self.grid_spacing = 30
        self.pen_grid = QPen(self.grid_color, 1, Qt.DotLine)

        self.setSceneRect(QRectF(-1000, -1000, 2000, 2000))
        self.setBackgroundBrush(self.bg_color)
        self.create_nodes()
        self.create_connections()
         
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        lines = []

        vertical_top = QPoint(rect.topLeft().toPoint())
        vertical_bottom = QPoint(rect.bottomLeft().toPoint())
        horizontal_right = QPoint(rect.topRight().toPoint())
        horizontal_left = QPoint(rect.topLeft().toPoint())

        for n in range(1000):
            lines.append(QLine(vertical_top, vertical_bottom))
            vertical_top.setX(vertical_top.x() + self.grid_spacing)
            vertical_bottom.setX(vertical_bottom.x() + self.grid_spacing)

        for n in range(1000):
            lines.append(QLine(horizontal_left, horizontal_right))
            horizontal_left.setY(horizontal_left.y() + self.grid_spacing)
            horizontal_right.setY(horizontal_right.y() + self.grid_spacing)

        painter.setPen(self.pen_grid)
        painter.drawLines(lines)

    def create_nodes(self):

        self.node = GraphicsNode(name="Node 001", port_pos=0)
        self.addItem(self.node)

        self.node_nr2 = GraphicsNode(name="Node 002", port_pos=1)
        self.addItem(self.node_nr2)
        
        self.line = GraphicsLine(self.node.port_pos().x(), self.node.port_pos().y(), self.node_nr2.port_pos().x(), self.node_nr2.port_pos().y())
        self.addItem(self.line)


    def create_connections(self):
        self.NodeMoved.connect(self.updateLine)

    def updateLine(self):
        self.line.end_point_x = self.node.port_pos().x()
        self.line.end_point_y = self.node.port_pos().y()
        self.line.start_point_x = self.node_nr2.port_pos().x()
        self.line.start_point_y = self.node_nr2.port_pos().y()
