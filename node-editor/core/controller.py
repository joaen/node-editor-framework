import os
import json
import traceback
from functools import partial
from PySide2.QtWidgets import QFileDialog
from graphics.graphics_node import GraphicsNode
from graphics.graphics_line import GraphicsLine
from graphics.graphics_port import GraphicsPort
from graphics.graphics_mouse_line import GraphicsMouseLine
from graphics.graphics_scene import EditorGraphicsScene
from PySide2.QtCore import Qt

from core.logic_node import LogicNode
from core.logic_port import LogicPort

from example_nodes.multiply_node import MultiplyNode # Example node
from example_nodes.float_node import FloatNode # Example node
from example_nodes.add_node import AddNode # Example node

class Controller():
    '''
    Controller for managing node operations in the node editor.
    
    This controller holds actions related to both logic and UI nodes, 
    acting as an intermediary to handle user inputs, update node states, and 
    reflect changes in the UI. This class holds functionalities like node creation, 
    deletion, and connection.
    '''
    def __init__(self, scene):
        self.scene: EditorGraphicsScene = scene
        self.connections = []
        self.nodes = {}
        self.node_ports = {}
        self.lines = []

        self.clicked_ports = []
        self.is_following_mouse = False
        self.graphics_mouse_line = None
        self.connect_signals()
        self.connect_keys()

    def connect_signals(self):
        self.scene.mouse_position_signal.connect(self.mouse_moved)
        self.scene.node_moved_signal.connect(self.ui_update_line)
        self.scene.port_pressed_signal.connect(self.ui_port_pressed)
        self.scene.port_text_changed_signal.connect(self.ui_port_text_changed)
        self.scene.clicked_view_signal.connect(self.ui_remove_mouse_line)

    def connect_keys(self):
        self.scene.create_key_event(Qt.Key_Delete, partial(self.delete_selected))

    def ui_remove_mouse_line(self):
        if self.is_following_mouse:
            self.is_following_mouse = False
            self.clicked_ports.clear()
            self.scene.removeItem(self.graphics_mouse_line)

    def mouse_moved(self, mouse_pos):
        if self.is_following_mouse:
            clicked_one, clicked_one_graphics = self.clicked_ports[0]
            self.graphics_mouse_line.update_pos(pos1=clicked_one_graphics.port_pos(), pos2=mouse_pos)
    
    def ui_port_text_changed(self, node_id, port, value):
        ports = self.node_ports.get(node_id)
        ports.get(port).data = value
        self.update_nodes()

    def ui_port_pressed(self, node_id, graphics_port):
        node_ports = self.node_ports.get(str(node_id))
        logic_port = node_ports.get(graphics_port)
        self.clicked_ports.append((logic_port, graphics_port))
        
        if len(self.clicked_ports) >= 2:
            self.scene.removeItem(self.graphics_mouse_line)
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            clicked_port_2, clicked_port_2_graphics = self.clicked_ports[1]
            self.connect_ports(clicked_port_1, clicked_port_2)
            self.is_following_mouse = False
            self.clicked_ports.clear()
        
        if len(self.clicked_ports) == 1:
            clicked_port_1, clicked_port_1_graphics = self.clicked_ports[0]
            self.graphics_mouse_line = GraphicsMouseLine(point_one=clicked_port_1_graphics.port_pos(), point_two=clicked_port_1_graphics.port_pos())
            self.graphics_mouse_line.setZValue(self.graphics_mouse_line.zValue() - 1)
            self.scene.addItem(self.graphics_mouse_line)
            self.is_following_mouse = True
        
    def ui_update_line(self):
        try:
            for line in self.lines:
                line.update_pos()
        except RuntimeError:
            traceback.print_exc()

    def connect_logic_ports(self, port1: LogicPort, port2: LogicPort):
        if port1.is_connected and port2.is_connected:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port1))
            return False
        if port2.is_connected and port2.is_input:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port1))
            return False
        if port1.is_connected and port1.is_input:
            print("THIS PORT ALREADY HAVE A CONNECTION".format(port1))
            return False
        elif port1 == port2:
            print("CAN'T CONNECT PORT TO ITSELF")
            return False
        elif port1.is_input and port2.is_input:
            print("YOU CAN'T CONNECT TWO INPUT PORTS")
            return False
        elif port1.is_input == False and port2.is_input == False:
            print("YOU CAN'T CONNECT TWO OUTPUT PORTS")
            return False
        elif port1.parent_node == port2.parent_node:
            print("YOU CAN'T CONNECT NODE TO ITSELF")
            return False
        else:
            port1.connection = port2
            port2.connection = port1
            port1.is_connected = True
            port2.is_connected = True
            port1.parent_node.connections.append(port2.parent_node)
            port2.parent_node.connections.append(port1.parent_node)
            print("Connected: {} || {}".format(port1.parent_node, port2.parent_node))
            return True

    def break_connection(self, port_1: LogicPort, port_2: LogicPort):
        if isinstance(port_1, LogicPort) and isinstance(port_2, LogicPort):
            port_1.connection = None
            port_2.connection = None
            port_1.is_connected = False
            port_2.is_connected = False

            ports_to_check = {port_1, port_2}
            self.connections = [connection for connection in self.connections if not ports_to_check.issubset(set(connection))]
            print("Broke connection between: {} AND {} ".format(port_1, port_2))
            return True
        else:
            print("CAN'T BREAK CONNECTION BETWEEN: {} AND {} ".format(port_1, port_2))
            return False

    def delete_node(self, node : LogicNode):
        node.exsist = False
        self.nodes.pop(node)
        print("Deleted node: {}".format(node))

    def create_logic_node(self, node_name):
        node_class = globals().get(node_name)

        if node_class and issubclass(node_class, LogicNode):
            logic_node = node_class()
            self.nodes[logic_node] = None
            return logic_node
        else:
            raise ValueError(f"No LogicNode subclass named {node_name} exists in the current namespace")

    def get_nodes_topological(self):
        visited = set()
        post_order = []
        source_nodes = []

        for logic_node in list(self.nodes.keys()):
            for port in list(logic_node.io_ports.values()):
                if port.is_connected:
                    break
                else:
                    source_nodes.append(logic_node)

        def visit(node):
            if node not in visited:
                visited.add(node)
                for connection in node.connections:
                    visit(connection)
                post_order.append(node)

        for node in source_nodes:
            visit(node)

        post_order.reverse()
        return post_order
    
    def new_scene(self):
        self.select_all_items()
        self.delete_selected()
        self.nodes.clear()
        self.node_ports.clear()

    def load_scene(self):
        data = self._load_json()
        if data:
            self.new_scene()
            for data_set in data:
                node_id = data_set.get("id")
                node_name = data_set.get("node_name")
                node_pos = data_set.get("pos")

                logic_node, graphics_node = self.create_node(node_name=node_name, id=node_id)
                graphics_node.setPos(node_pos[0], node_pos[1])
            
            for data_set in data:
                connections = data_set.get("connections") 
                port_data = data_set.get("port_data")

                if port_data:
                    for port, data in port_data.items():
                        port_parent = port.split(".")[0]
                        port_name = port.split(".")[1]
                        for node, ui_node in self.nodes.items():
                            if port_parent == node.id:
                                node.io_ports.get(port_name).data = data    
                                self.update_nodes()

                if connections:
                    for connection in connections:
                        port1, port2 = connection
                        port1_parent = port1.split(".")[0]
                        port2_parent = port2.split(".")[0]
                        port1_name = port1.split(".")[1]
                        port2_name = port2.split(".")[1]

                        connect_ports = []
                        for node, ui_node in self.nodes.items():
                            if port1_parent == node.id:
                                ports = self.node_ports.get(node.id)
                                for ui_port, logic_port in ports.items():
                                    if logic_port.name == port1_name:
                                        connect_ports.append(logic_port)
                            elif port2_parent == node.id:
                                ports = self.node_ports.get(node.id)
                                for ui_port, logic_port in ports.items():
                                    if logic_port.name == port2_name:
                                        connect_ports.append(logic_port)
                        self.connect_ports(connect_ports[0], connect_ports[1])
        
    def _load_json(self):
        file_path = QFileDialog.getOpenFileName(None, "Load scene", os.path.dirname(os.path.abspath(__file__)), "Scene file (*.json);;All files (*.*)")
        if file_path[0]:
            import json
            with open(file_path[0], "r") as file:
                data = json.load(file)
            return data

    def save_scene(self):
        file_path = QFileDialog.getSaveFileName(None, "Save scene", os.path.dirname(os.path.abspath(__file__)), "Scene file (*.json);;All files (*.*)")
        if file_path[0]:
            data = []

            for node in self.nodes.keys():
                connections = []
                input_port_data = {}
                for port in node.io_ports.values():
                    if port.is_input:
                        input_port_data["{}.{}".format(node.id, port.name)] = port.data
                        if port.is_connected:
                            connections.append(["{}.{}".format(node.id, port.name), "{}.{}".format(port.connection.parent_node.id, port.connection.name)])

                graphics_node = self.nodes.get(node)
                node_data = {"id" : node.id,
                            "node_name" : str(type(node).__name__),
                            "pos" : [graphics_node.pos().x(), graphics_node.pos().y()],
                            "connections" : connections,
                            "port_data" : input_port_data}
                data.append(node_data)

            with open(file_path[0], 'w') as file:
                json.dump(data, file, indent=2)

    def select_all_items(self):
        for item in self.scene.items():
            item.setSelected(True)

    def delete_selected(self):
        all_ports = {key: value for inner_dict in self.node_ports.values() for key, value in inner_dict.items()}
        try:
            lines_to_remove = set()
            for item in self.scene.selectedItems():
                if isinstance(item, GraphicsLine):
                    deleted_connection = self.break_connection(all_ports.get(item.port_one), all_ports.get(item.port_two))
                    if deleted_connection:
                        lines_to_remove.add(item)

                if isinstance(item, GraphicsNode):
                    for node in self.nodes.keys():
                        if self.nodes.get(node) == item:
                            self.delete_node(node)
                            break
                    self.scene.removeItem(item)
            
            for line in self.lines:
                if line.port_one.parent_node.scene() == None or line.port_two.parent_node.scene() == None:
                    removed_connection = self.break_connection(all_ports.get(line.port_one), all_ports.get(line.port_two))
                    if removed_connection:
                        lines_to_remove.add(line)

            for line in list(lines_to_remove):
                self.lines.remove(line)
                self.scene.removeItem(line)
        
        except RuntimeError:
            traceback.print_exc()

    def create_line(self, port_one : GraphicsPort, port_two : GraphicsPort):
        line = GraphicsLine(port_one=port_one, port_two=port_two)
        line.setZValue(line.zValue() - 1)
        self.lines.append(line)
        self.scene.addItem(line)

    def connect_ports(self, port1: LogicPort, port2: LogicPort):
        connection = self.connect_logic_ports(port1, port2)
        ports_to_connect = []
        if connection:
            for id, ports in self.node_ports.items():
                for ui_port, logic_port in ports.items():
                    if logic_port == port1:
                        ports_to_connect.append(ui_port)
                    if logic_port == port2:
                        ports_to_connect.append(ui_port)
            self.create_line(ports_to_connect[0], ports_to_connect[1])
            self.connections.append((port1, ports_to_connect[0], port2, ports_to_connect[1]))
            self.update_nodes()

    def create_node(self, node_name, id=None):
        try:
            logic_node = self.create_logic_node(node_name)
            node_id = (lambda: logic_node.id if id == None else id)()
            logic_node.id = node_id
            graphics_node = GraphicsNode(name=logic_node.NAME, id=logic_node.id, header_color=logic_node.node_color, default_value=logic_node.default_value)
            ports = graphics_node.create_ports(ports=logic_node.io_ports)
            self.scene.addItem(graphics_node)
            self.nodes[logic_node] = graphics_node
            self.node_ports[str(logic_node.id)] = ports
            return logic_node, graphics_node
        except RuntimeError:
            traceback.print_exc()

    def update_nodes(self):
        try:
            for node in self.get_nodes_topological():
                node.execute()
                ports = self.node_ports.get(node.id)

                for ui_port, logic_port in ports.items():
                    ui_port.set_input_text(logic_port.data)
        except RuntimeError:
            traceback.print_exc()