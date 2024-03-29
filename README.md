# Python + PySide2 Node Editor
Node editor framework which can be used as a standalone application or integrated into Python + PySide2 projects.

![anim_node](https://github.com/joaen/node-editor-framework/assets/6629861/c152faed-7729-4389-9df3-884e0464bb9d)

# Compatibility
* This application was created using **Python 3.10.11**.
* Tested with Windows 10 and OSX v10.12.

 # Dependencies
* PySide2==5.15.2.1
* shiboken2==5.15.2.1

To install the dependencies in your current environment you can run the following snippet:
```
pip install -r requirements.txt
```

# How to use
* Start the application by running main.py (Make sure the dependencies have been installed first).

Command           | Key binding    
---| ---
Open context menu | RMB            
Focus on selected | F              
Delete selected   | Del            
Pan scene view    | MMB            
Zoom in/out       | Scroll up/down 

* The context menu contains these actions:

![image](https://github.com/joaen/node-editor-framework/assets/6629861/0e9d3e7c-38f8-419e-94e7-e2e899fe7308)


# How to create a custom nodes
To create your own custom node you can simply create new child class of the abstract class ***LogicNode*** and use it as a template.

In your new class need to define and declare a few things:
1. The name of the node, using the constant ***NAME*** attribute.
2. An unique id for the node, using the ***id*** variable (Preferrebly using uuid like the LogicNode class).
3. An empty list where the node can store its connections, using the ***connections*** variable. This is used for determine the node evaluation order.
4. The UI color of the node, using the ***node_color*** variable.
5. The input/output, using the ***io_ports*** variable. This variable should be a dict. The keys in the dict should be a string and the values should be an instance of the ***LogicPort*** class.
6. You also need to define a ***execute*** method which should hold the actual expression of the node and then pass that data to the output port. For example, a multiply expression node would have the ***execute*** look something like this:
> output_port.data = (input1_port.data + input2_port.data)

Here is an example on how you can create your own expression node:

```python
import uuid
from core.logic_port import LogicPort

class ExampleNode(LogicNode):

    NAME = "My Custom Node" # Name of the node displayed in the UI.

    def __int__(self):
        self.id = uuid.uuid4() # The node need an unique id for save/load functionality to work
        self.node_color = (255, 255, 255) # Color of the node displayed in the UI.
        self.connections = [] # Used in runtime to determine evaluation order of the connected nodes.

        # Declare io ports by adding a dict with name keys and instances of LogicPort as values.
        self.io_ports = {"Input" : LogicPort(is_input=True), "Output" : LogicPort(is_input=False)}

    def execute(self):
        ''' 
        This is where the node operation is done and then passed to the output port.
        '''
        output_port = self.io_ports.get("Output")
        output_port.data = (5 + 5)

```

To make the custom node show up in the scene in the application you need to call the **create_node** method of the controller class and pass the name of your node class.

```python
controller = Controller(scene)
controller.create_node("ExampleNode")
```

The example nodes in the applications are created by connecting the create_node method to a context menu action. Like this:

```python
self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "AddNode"), "Add Node")
```







