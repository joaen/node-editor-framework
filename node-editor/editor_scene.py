from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class EditorGraphicsScene(QGraphicsScene):

    NodeMoved = Signal(QPointF)

    def __init__(self):
        super().__init__()

        self.bg_color = QColor(90, 90, 90)
        self.grid_color = QColor(150, 150, 150)
        self.grid_spacing = 30

        self.pen_grid = QPen(self.grid_color)
        self.pen_grid.setWidth(1)

        self.scene_size = [1000, 1000]
        self.setSceneRect(0, 0, self.scene_size[0], self.scene_size[1])
        self.setBackgroundBrush(self.bg_color)
         
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