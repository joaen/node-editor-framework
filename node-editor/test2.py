import sys
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsLineItem
from PySide2.QtCore import Qt, QPointF, Signal, QLineF
from PySide2.QtGui import QPen

# Create a QApplication instance before creating any widgets
app = QApplication(sys.argv)

class CircleItem(QGraphicsEllipseItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRect(-25, -25, 50, 50)
        self.setBrush(Qt.red)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # Emit a signal to notify the main window that the circle has moved
        self.scene().circleMoved.emit(self.pos())

class SquareItem(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRect(-25, -25, 10, 10)
        self.setBrush(Qt.green)

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

        # Create a line item connecting the circle and square
        self.line = QGraphicsLineItem()
        self.line.setPen(QPen(Qt.black))
        self.scene.addItem(self.line)

        # Connect the circleMoved signal to the updateLine method
        self.scene.circleMoved.connect(self.updateLine)

    def updateLine(self, pos):
        # Update the position of the line item
        self.line.setLine(QLineF(pos, self.square.pos()))

if __name__ == '__main__':
    # Create and show the main window
    window = MainWindow()
    window.show()

    # Enter the application event loop
    sys.exit(app.exec_())
