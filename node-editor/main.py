import sys
from PySide2.QtWidgets import *
# from main_window import MainWindow
from editor_scene import QEditorGraphicsScene
from editor_view import QEditorGraphicsView
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Editor")
        # self.setFixedSize(QSize(400, 300))
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_debug_content()

    def create_ui_widgets(self):
        self.scene = QEditorGraphicsScene()
        self.view = QEditorGraphicsView(self.scene)
        self.view.setScene(self.scene)


    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

    def create_debug_content(self):
        square = self.scene.addRect(300, 500, 80, 100, QPen(Qt.black), QBrush(Qt.green))
        square.setFlag(QGraphicsItem.ItemIsMovable)
        square.setFlag(QGraphicsItem.ItemIsSelectable)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
