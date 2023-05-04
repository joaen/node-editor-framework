import PySide2.QtGui
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class QEditorGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__()
        self.graphics_scene = scene
        self.zoom = 0

        self.setScene(self.graphics_scene)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
    # PC ???? 
    # def create_ui(self):
        # self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    # def mousePressEvent(self, event: QMouseEvent):
    #     if event.button() ==  Qt.RightButton:
    #         self.setDragMode(QGraphicsView.ScrollHandDrag)
    #     else:
    #         return super().mouseDoubleClickEvent(event)
    
    # def mouseReleaseEvent(self, event: QMouseEvent):
    #     if event.button() == Qt.RightButton:
    #         self.setDragMode(QGraphicsView.NoDrag)
    #     else:
    #         return super().mouseReleaseEvent(event)
        
    # MAC *****
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            QApplication.setOverrideCursor(Qt.OpenHandCursor)
            self.__prevMousePos = event.pos()
        else:
            return super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        else:
            return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)
            offset = self.__prevMousePos - event.pos()
            self.__prevMousePos = event.pos()

            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
        else:
            return super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.05
            self.zoom += 1
        else:
            factor = 0.95
            self.zoom -= 1
        self.scale(factor, factor)