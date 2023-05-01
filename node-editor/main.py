import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton
# from main_window import MainWindow
from editor_scene import QEditorGraphicsScene
from PySide2.QtCore import QSize
from PySide2.QtWidgets import *


# Subclass QMainWindow to customize your application's main window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Node Editor")
        # self.setFixedSize(QSize(400, 300))

        self.create_ui_widgets()
        self.create_ui_layout()

    def create_ui_widgets(self):
        self.scene = QEditorGraphicsScene()
        self.view = QGraphicsView()
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
