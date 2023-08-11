from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QMouseEvent
from PySide2.QtWidgets import QGraphicsView, QApplication


class EditorGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__()
        self.graphics_scene = scene
        self.zoom = 0

        self.setScene(self.graphics_scene)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)

        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item is None:
                self.scene().clicked_view_signal.emit()
        if event.button() == Qt.MiddleButton:
            QApplication.setOverrideCursor(Qt.OpenHandCursor)
            self.__prevMousePos = event.pos()
        else:
            return super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MiddleButton:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        else:
            return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MiddleButton:
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