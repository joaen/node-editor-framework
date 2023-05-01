from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class QEditorGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        self.bg_color = QColor(90, 90, 90)
        self.grid_color = QColor(150, 150, 150)
        self.grid_spacing = 20

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

        for n in range(200):
            lines.append(QLine(vertical_top, vertical_bottom))
            vertical_top.setX(vertical_top.x() + 20)
            vertical_bottom.setX(vertical_bottom.x() + 20)

        for n in range(200):
            lines.append(QLine(horizontal_left, horizontal_right))
            horizontal_left.setY(horizontal_left.y() + 20)
            horizontal_right.setY(horizontal_right.y() + 20)

  

        painter.setPen(self.pen_grid)
        painter.drawLines(lines)