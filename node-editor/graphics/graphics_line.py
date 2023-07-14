from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics.graphics_port import GraphicsPort


class GraphicsLine(QGraphicsPathItem):

    def __init__(self, port_one : GraphicsPort, port_two : GraphicsPort, connection_list):
        super().__init__()
        self.connection = connection_list
        self.port_one = port_one
        self.port_two = port_two
        self.start_point_x = self.port_one.port_pos().x()
        self.start_point_y = self.port_one.port_pos().y()
        self.end_point_x = self.port_two.port_pos().x()
        self.end_point_y = self.port_two.port_pos().y()
        self.line_path = QPainterPath()
        self.color = QColor(255, 255, 255)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scene().line_pressed_signal.emit(self.connection, self)
            print("CLICKED LINE")
        else:
            super().mousePressEvent(event)

    def boundingRect(self):
        return self.line_path.boundingRect()

    def paint(self, painter: QPainter, option, widget=None):

        if self.isSelected():
            pen = QPen(QColor(0, 255, 0))
        else:
            pen = QPen(self.color)
            
        pen.setWidth(4)
        painter.setPen(pen)

        start_point = QPointF(self.start_point_x, self.start_point_y)
        self.line_path.moveTo(start_point)

        if self.port_one.is_input == True:
            point1 = QPointF((self.start_point_x - 100), self.start_point_y)
        else:
            point1 = QPointF((self.start_point_x + 100), self.start_point_y)
        
        if self.port_two.is_input == True:
            point2 = QPointF((self.end_point_x - 100), self.end_point_y)
        else:
            point2 = QPointF((self.end_point_x + 100), self.end_point_y)

        end_point = QPointF(self.end_point_x, self.end_point_y)
        self.line_path.cubicTo(point1, point2, end_point)
        painter.drawPath(self.shape())
        self.setPath(self.line_path)

    def shape(self):
        return self.line_path
    
    def update_pos(self):
        self.line_path.clear()
        self.start_point_x = self.port_one.port_pos().x()
        self.start_point_y = self.port_one.port_pos().y()
        self.end_point_x = self.port_two.port_pos().x()
        self.end_point_y = self.port_two.port_pos().y()
        self.update()
        