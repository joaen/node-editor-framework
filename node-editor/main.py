import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from graphics.scene import EditorGraphicsScene
from graphics.view import EditorGraphicsView
from graphics.node import GraphicsNode
from graphics.line import GraphicsLine


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Editor")
        self.setBaseSize(QSize(600, 600))
        self.create_ui_widgets()
        self.create_ui_layout()

    def create_ui_widgets(self):
        self.scene = EditorGraphicsScene()
        self.view = EditorGraphicsView(self.scene)
        self.view.setScene(self.scene)

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
