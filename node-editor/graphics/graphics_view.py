from PySide2 import QtCore, QtWidgets, QtGui


class EditorGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, scene):
        super().__init__()
        self.graphics_scene = scene
        self.zoom = 0

        self.setScene(self.graphics_scene)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing)

        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item is None:
                self.scene().clicked_view_signal.emit()
        if event.button() == QtCore.Qt.MiddleButton:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.OpenHandCursor)
            self.__prevMousePos = event.pos()
        else:
            return super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.MiddleButton:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)
        else:
            return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MiddleButton:
            QtCore.QApplication.setOverrideCursor(QtCore.Qt.ClosedHandCursor)
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