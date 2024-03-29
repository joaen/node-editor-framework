from PySide2.QtCore import QPointF
from PySide2.QtGui import QPainter, QPen, QPainterPath, QColor
from PySide2.QtWidgets import QGraphicsPathItem


class GraphicsMouseLine(QGraphicsPathItem):

    def __init__(self, point_one : QPointF, point_two : QPointF):
        super().__init__()
        self.point_one = point_one
        self.point_two = point_two
        self.line_path = None
        self.color = QColor(150, 150, 150)

    def paint(self, painter: QPainter, option, widget=None):
        self.line_path = QPainterPath()
        pen = QPen(self.color)
            
        pen.setWidth(4)
        painter.setPen(pen)

        self.line_path.moveTo(self.point_one)

        self.line_path.cubicTo(self.point_one, self.point_two, self.point_two)
        painter.drawPath(self.line_path)
        self.setPath(self.line_path)
    
    def update_pos(self, pos1, pos2):
        self.line_path.clear()
        self.point_one = pos1
        self.point_two = QPointF(pos2.x(), pos2.y() + 8)
        self.update()
        