import sys
import traceback
from PySide2.QtWidgets import QHBoxLayout, QWidget, QStyle, QApplication
from PySide2.QtCore import QSize, Qt
from functools import partial
from core.controller import Controller
from graphics.graphics_scene import EditorGraphicsScene
from graphics.graphics_view import EditorGraphicsView
from graphics.graphics_mouse_line import GraphicsMouseLine


class MainWindow(QWidget): 
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.setWindowTitle("Node Editor")
        self.setBaseSize(QSize(600, 600))
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        self.clicked_ports = []
        self.is_following_mouse = False
        self.graphics_mouse_line = None
    
    def create_ui_widgets(self):
        scene = EditorGraphicsScene()
        self.view = EditorGraphicsView(scene)
        self.view.setScene(scene)
        self.controller.scene = scene

    def create_ui_layout(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

    def create_ui_connections(self):
        self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "AddNode"), "Add Node")
        self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "MultiplyNode"), "Multiply Node")
        self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "FloatNode"), "Float Node")

        self.controller.scene.contextMenu.addSeparator()
        save_action = self.controller.scene.add_contextmenu_item(self.controller.save_scene, "Save Scene")
        load_action = self.controller.scene.add_contextmenu_item(self.controller.load_scene, "Load Scene")
        save_action.setIcon(app.style().standardIcon(QStyle.SP_DialogSaveButton))
        load_action.setIcon(app.style().standardIcon(QStyle.SP_DialogOpenButton))

        self.controller.scene.create_key_event(Qt.Key_Delete, partial(self.controller.deleted_selected))
        self.controller.scene.mouse_position_signal.connect(self.mouse_moved)
        self.controller.scene.node_moved_signal.connect(self.ui_update_line)
        self.controller.scene.port_pressed_signal.connect(self.ui_port_pressed)
        self.controller.scene.port_text_changed_signal.connect(self.ui_port_text_changed)
        self.controller.scene.clicked_view_signal.connect(self.ui_remove_mouse_line)

    def ui_remove_mouse_line(self):
        if self.is_following_mouse:
            self.is_following_mouse = False
            self.clicked_ports.clear()
            self.controller.scene.removeItem(self.graphics_mouse_line)

    def mouse_moved(self, mouse_pos):
        if self.is_following_mouse == True:
            clicked_one, clicked_one_graphics = self.clicked_ports[0]
            self.graphics_mouse_line.update_pos(pos1=clicked_one_graphics.port_pos(), pos2=mouse_pos)

    def ui_port_text_changed(self, port, value):
        port.data = value
        self.controller.update_nodes()   

    def ui_port_pressed(self, port_id, graphics_port):  
        self.clicked_ports.append((port_id, graphics_port))
        
        if len(self.clicked_ports) >= 2:
            self.controller.scene.removeItem(self.graphics_mouse_line)
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            clicked_port_2, clicked_port_2_graphics = self.clicked_ports[1]

            self.controller.connect_ports(clicked_port_1, clicked_port_2)
            self.is_following_mouse = False
            self.clicked_ports.clear()
        
        if len(self.clicked_ports) == 1:
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            self.graphics_mouse_line = GraphicsMouseLine(point_one=clicked_port_1_graphics.port_pos(), point_two=clicked_port_1_graphics.port_pos())
            self.graphics_mouse_line.setZValue(self.graphics_mouse_line.zValue() - 1)
            self.controller.scene.addItem(self.graphics_mouse_line)
            self.is_following_mouse = True
        
    def ui_update_line(self):
        try:
            for line in self.controller.lines:
                line.update_pos()
        except:
            traceback.print_exc()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()