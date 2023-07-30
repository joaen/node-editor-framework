import sys
import os
import json
import traceback
from PySide2 import QtCore, QtWidgets
from functools import partial
from graphics.graphics_scene import EditorGraphicsScene
from graphics.graphics_view import EditorGraphicsView
from graphics.graphics_line import GraphicsLine
from graphics.graphics_node import GraphicsNode
from graphics.graphics_port import GraphicsPort
from graphics.graphics_mouse_line import GraphicsMouseLine
from core.controller import Controller
from core.logic_port import LogicPort


class MainWindow(QtWidgets.QWidget): 
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.setWindowTitle("Node Editor")
        self.setBaseSize(QtCore.QSize(600, 600))
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()

        self.lines = []
        self.clicked_ports = []
        self.is_following_mouse = False
        self.graphics_mouse_line = None

        # self.create_add_node()
        # self.create_add_node()
    
    def create_ui_widgets(self):
        self.scene = EditorGraphicsScene()
        self.view = EditorGraphicsView(self.scene)
        self.view.setScene(self.scene)

    def create_ui_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.view)

    def create_ui_connections(self):
        self.scene.add_contextmenu_item(self.create_add_node, "Add Node")
        self.scene.add_contextmenu_item(self.create_multiply_node, "Multiply Node")
        self.scene.add_contextmenu_item(self.create_float_node, "Float Node")
        self.scene.add_contextmenu_item(self.save_scene, "Save Scene")
        self.scene.add_contextmenu_item(self.load_scene, "Load Scene")
        self.scene.create_key_event(QtCore.Qt.Key_Delete, partial(self.deleted_selected))
        self.scene.mouse_position_signal.connect(self.mouse_moved)
        self.scene.node_moved_signal.connect(self.update_line)
        self.scene.port_pressed_signal.connect(self.port_pressed)
        self.scene.port_text_changed_signal.connect(self.port_text_changed)
        self.scene.clicked_view_signal.connect(self.clear_mouse_line)

    def clear_mouse_line(self):
        if self.is_following_mouse:
            self.is_following_mouse = False
            self.clicked_ports.clear()
            self.scene.removeItem(self.graphics_mouse_line)

    def port_text_changed(self, port, value):
        port.data = value
        self.update_nodes()

    def mouse_moved(self, mouse_pos):
        if self.is_following_mouse == True:
            clicked_one, clicked_one_graphics = self.clicked_ports[0]
            self.graphics_mouse_line.update_pos(pos1=clicked_one_graphics.port_pos(), pos2=mouse_pos)

    def create_multiply_node(self):
        logic_node = self.controller.create_node("MultiplyNode")
        graphics_node = GraphicsNode.create_ui_node(logic_node, scene=self.scene)
        self.controller.nodes[logic_node] = graphics_node

    def create_float_node(self):
        logic_node = self.controller.create_node("FloatNode")
        graphics_node = GraphicsNode.create_ui_node(logic_node, scene=self.scene)
        self.controller.nodes[logic_node] = graphics_node

    def create_add_node(self):
        logic_node = self.controller.create_node("AddNode")
        graphics_node = GraphicsNode.create_ui_node(logic_node, scene=self.scene)
        self.controller.nodes[logic_node] = graphics_node

    def update_nodes(self):
        for node in self.controller.nodes.keys():
            node.update()
            ports = self.controller.nodes.get(node).ports
            for logic_port in ports.keys():
                if logic_port.is_input == False:
                    ports.get(logic_port).set_input_text(ports.get(logic_port).port_id.data)
        
        for connection in self.controller.connections:
            port_1, port_1_shape, port_2, port_2_shape = connection
            if port_1.is_input:
                port_1_shape.set_input_text(port_2_shape.port_id.data)
            if port_2.is_input:
                port_2_shape.set_input_text(port_1_shape.port_id.data)

    def create_connection(self, port1: LogicPort, port2: LogicPort):
        connection = Controller.create_connection(port1, port2)
        if connection:
            ports_to_connect = []
            for ui_node in self.controller.nodes.values():
                for logic_port, ui_port in ui_node.ports.items():
                    if logic_port == port1:
                        ports_to_connect.append(ui_port)
                    if logic_port == port2:
                        ports_to_connect.append(ui_port)

            self.create_line(ports_to_connect[0], ports_to_connect[1])
            self.controller.connections.append((port1, ports_to_connect[0], port2, ports_to_connect[1]))
                    
    def get_key(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None    

    def port_pressed(self, port_id, graphics_port):  
        self.clicked_ports.append((port_id, graphics_port))
        
        if len(self.clicked_ports) >= 2:
            self.scene.removeItem(self.graphics_mouse_line)
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            clicked_port_2, clicked_port_2_graphics = self.clicked_ports[1]

            self.create_connection(clicked_port_1, clicked_port_2)
            self.is_following_mouse = False
            self.clicked_ports.clear()
        
        if len(self.clicked_ports) == 1:
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            self.graphics_mouse_line = GraphicsMouseLine(point_one=clicked_port_1_graphics.port_pos(), point_two=clicked_port_1_graphics.port_pos())
            self.graphics_mouse_line.setZValue(self.graphics_mouse_line.zValue() - 1)
            self.scene.addItem(self.graphics_mouse_line)
            self.is_following_mouse = True

    def create_line(self, port_one : GraphicsPort, port_two : GraphicsPort):
        line = GraphicsLine(port_one=port_one, port_two=port_two)
        line.setZValue(line.zValue() - 1)
        self.lines.append(line)
        self.scene.addItem(line)
        self.update_line()

    def select_all_items(self):
        for item in self.scene.items():
            item.setSelected(True)

    def deleted_selected(self):
        try:
            for item in self.scene.selectedItems():
                if isinstance(item, GraphicsLine):
                    Controller.break_connection(item.port_one.port_id, item.port_two.port_id)
                    self.scene.removeItem(item)
                if isinstance(item, GraphicsNode):
                    for node in self.controller.nodes.keys():
                        if self.controller.nodes.get(node) == item:
                            self.controller.delete_node(node)
                            break
                    self.scene.removeItem(item)
            
            for line in self.lines:
                if line.port_one.parent_node.scene() == None or line.port_two.parent_node.scene() == None:
                        self.scene.removeItem(line)
                        Controller.break_connection(line.port_one, line.port_two)
        except:
            traceback.print_exc()
        
    def update_line(self):
        try:
            for line in self.lines:
                line.update_pos()
        except:
            pass

    def load_scene(self):
        self.select_all_items()
        self.deleted_selected()
        data = self.load_json()
        if data:
            for data_set in data:
                node_id = data_set.get('id')
                node_name = data_set.get('node_name')
                node_pos = data_set.get('pos')

                logic_node = self.controller.create_node(node_name)
                graphics_node = GraphicsNode.create_ui_node(logic_node, scene=self.scene)
                self.controller.nodes[logic_node] = graphics_node

                logic_node.id = node_id
                graphics_node.setPos(node_pos[0], node_pos[1])
            
            for data_set in data: 
                connections = data_set.get('connections') 
                if connections:
                    for connection in connections:
                        print(connection)
                        port1 : str
                        port2 : str
                        port1, port2 = connection

                        port1_parent = port1.split(".")[0]
                        port2_parent = port2.split(".")[0]
                        port1_name = port1.split(".")[1]
                        port2_name = port2.split(".")[1]

                        connect_ports = []
                        for node, ui_node in self.controller.nodes.items():
                            if port1_parent == node.id:
                                for port, ui_port in ui_node.ports.items():
                                    if port.name == port1_name:
                                        connect_ports.append((port, ui_port))
                            if port2_parent == node.id:
                                for port, ui_port in ui_node.ports.items():
                                    if port.name == port2_name:
                                        connect_ports.append((port, ui_port))

                        self.create_connection(connect_ports[0][0], connect_ports[1][0])
        else:
            pass
        
    def load_json(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Load scene", os.path.dirname(os.path.abspath(__file__)), "Scene file (*.json);;All files (*.*)")
        if file_path[0]:
            import json
            with open(file_path[0], 'r') as file:
                data = json.load(file)
            return data

    def save_scene(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save scene", os.path.dirname(os.path.abspath(__file__)), "Scene file (*.json);;All files (*.*)")
        if file_path[0]:
            data = []

            for node in self.controller.nodes.keys():
                connections = []
                for port in node.input_ports.values():
                    if port.is_connected:
                        connections.append(["{}.{}".format(node.id, port.name,), "{}.{}".format(port.connection.parent_node.id, port.connection.name)])

                graphics_node = self.controller.nodes.get(node)
                node_data = {"id" : str(node.id), "node_name" : str(type(node).__name__), "pos" : [graphics_node.pos().x(), graphics_node.pos().y()], "connections" : connections}
                data.append(node_data)

            with open(file_path[0], 'w') as file:
                json.dump(data, file, indent=2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()