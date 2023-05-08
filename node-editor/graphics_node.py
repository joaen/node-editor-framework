from PySide2.QtCore import *
import PySide2.QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from graphics_circle import GraphicsCircle
from graphics_rect import GraphicsRect
from graphics_line import GraphicsLine


class GraphicsNode(QGraphicsItem):

    def __init__(self, line : GraphicsLine):
        super().__init__()
        self.line = line
        self.text = QLabel("WIWOWOWOOWOWOWOWWW")        
        self.proxy = QGraphicsProxyWidget(parent=self)
        self.proxy.setWidget(self.text)
        self.proxy.setPos(0, 0)
        self.proxy.setZValue(self.zValue() + 1)

        self.node_shape = GraphicsRect()
        self.node_shape.setParentItem(self)

        self.port_shape = GraphicsCircle()
        self.port_shape.setParentItem(self)
        self.port_shape.setPos(0, 100)

    def boundingRect(self):
        return self.port_shape.boundingRect().united(self.node_shape.boundingRect())

    def paint(self, painter, option, widget):
        pass

    # def port_pos(self):
    #     # world_pos = self.port_shape.mapToScene(self.port_shape.pos())
    #     scene_pos = self.port_shape.scenePos()
    #     return scene_pos
    # def sceneEventFilter(self, obj, event):
    #     if obj == self and event.type() == QEvent.GraphicsSceneMouseMove:
    #         # Update the child item's position
    #         # self.child.setPos(self.pos())
    #         self.line.end_point_x = self.port_shape.scenePos().x()
    #         self.line.end_point_y = self.port_shape.scenePos().y()

    #     return super().sceneEventFilter(obj, event)
    
    def sceneEvent(self, event):
        if event.type() == event.GraphicsSceneMouseMove:
            # print("What")
            # self.update()
            self.line.end_point_x = self.port_shape.scenePos().x()
            self.line.end_point_y = self.port_shape.scenePos().y()

        return super().sceneEvent(event)