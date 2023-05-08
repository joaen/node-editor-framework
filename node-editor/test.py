import sys
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsEllipseItem, QGraphicsRectItem
from PySide2.QtCore import Qt, QPointF, Signal
from PySide2.QtGui import QColor

# Create a QApplication instance before creating any widgets
app = QApplication(sys.argv)

class CircleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRect(-25, -25, 50, 50)
        self.setBrush(QColor(255, 0, 0))
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Emit a signal to notify the main window that the circle has moved
        self.scene().circleMoved.emit(self.pos())

class SquareItem(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRect(-25, -25, 10, 10)
        self.setBrush(QColor(0, 255, 0))

    def updatePosition(self, pos):
        self.setPos(pos)

class GraphicsScene(QGraphicsScene):
    # Define a signal that will be emitted when the circle is moved
    circleMoved = Signal(QPointF)

class MainWindow(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Create a scene
        self.scene = GraphicsScene()
        self.setScene(self.scene)

        # Create a circle and a square item
        self.circle = CircleItem()
        self.square = SquareItem()

        # Add the items to the scene
        self.scene.addItem(self.circle)
        self.scene.addItem(self.square)

        # Connect the circleMoved signal to the updatePosition method of the square item
        self.scene.circleMoved.connect(self.square.updatePosition)

if __name__ == '__main__':
    # Create and show the main window
    window = MainWindow()
    window.show()

    # Enter the application event loop
    sys.exit(app.exec_())
