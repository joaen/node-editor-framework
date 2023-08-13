import sys
from PySide2.QtWidgets import QHBoxLayout, QWidget, QStyle, QApplication
from PySide2.QtCore import QSize
from PySide2.QtGui import QFont, QGuiApplication
from functools import partial
from core.controller import Controller
from graphics.graphics_scene import EditorGraphicsScene
from graphics.graphics_view import EditorGraphicsView


class MainWindow(QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Editor")
        self.setBaseSize(QSize(600, 600))
        self.create_editor_scene()
        self.create_ui_layout()
        self.create_ui_connections()
    
    def create_editor_scene(self):
        scene = EditorGraphicsScene()
        self.view = EditorGraphicsView(scene)
        self.view.setScene(scene)
        self.controller = Controller(scene)

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

    def create_ui_connections(self):
        self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "AddNode"), "Add Node")
        self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "MultiplyNode"), "Multiply Node")
        self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "FloatNode"), "Float Node")
        self.controller.scene.contextMenu.addSeparator()
        new_action = self.controller.scene.add_contextmenu_item(self.controller.new_scene, "New Scene")
        save_action = self.controller.scene.add_contextmenu_item(self.controller.save_scene, "Save Scene")
        load_action = self.controller.scene.add_contextmenu_item(self.controller.load_scene, "Load Scene")
        save_action.setIcon(app.style().standardIcon(QStyle.SP_DialogSaveButton))
        load_action.setIcon(app.style().standardIcon(QStyle.SP_DialogOpenButton))
        new_action.setIcon(app.style().standardIcon(QStyle.SP_FileIcon))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen_dpi = QGuiApplication.primaryScreen().logicalDotsPerInch()
    font_size = int(12 * screen_dpi / 96)
    default_font = app.font()
    default_font.setPointSize(font_size)
    app.setFont(default_font)

    window = MainWindow()
    window.show()
    app.exec_()