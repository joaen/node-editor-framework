import sys
from PySide2.QtWidgets import *
from editor_scene import EditorGraphicsScene
from editor_view import EditorGraphicsView
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphics_node import GraphicsNode
from graphics_line import GraphicsLine

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Editor")
        # self.setFixedSize(QSize(400, 300))
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_debug_content()

    def create_ui_widgets(self):
        self.graphics_scene = EditorGraphicsScene()
        self.graphics_view = EditorGraphicsView(self.graphics_scene)
        self.graphics_view.setScene(self.graphics_scene)

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.graphics_view)

    def create_debug_content(self):
        node = GraphicsNode()
        self.graphics_scene.addItem(node)
        node.setFlag(QGraphicsItem.ItemIsMovable)

        # x, y = node.port_pos()
        # print(x)
        # print(y)
        # print(node.port_pos()[0])
        line = GraphicsLine(node)
        self.graphics_scene.addItem(line)
        # line.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
