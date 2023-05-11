import sys
from editor_scene import EditorGraphicsScene
from editor_view import EditorGraphicsView
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphics_node import GraphicsNode
from graphics_line import GraphicsLine
from graphics_circle import GraphicsCircle

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Editor")
        self.setFixedSize(QSize(600, 600))
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_debug_content()
        self.create_connections()

    def create_ui_widgets(self):
        self.scene = EditorGraphicsScene()
        self.view = EditorGraphicsView(self.scene)
        self.view.setScene(self.scene)

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

    def create_debug_content(self):

        self.line = GraphicsLine()
        self.scene.addItem(self.line)
        self.scene.addItem(self.line)

        self.node = GraphicsNode()
        self.scene.addItem(self.node)
        self.node.setFlag(QGraphicsItem.ItemIsMovable)

    def create_connections(self):
        self.scene.NodeMoved.connect(self.updateLine)

    def updateLine(self):
        self.line.end_point_x = self.node.pos().x()
        self.line.end_point_y = self.node.pos().y()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
