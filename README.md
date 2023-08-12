# Python + PySide2 Node Editor
Node editor framework which can be used as a standalone application or integrated into Python + PySide2 projects.

![Animation](https://github.com/joaen/node-editor-framework/assets/6629861/51a84e31-ebde-419b-9013-a154e5efb311)

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
* Use mouse right-click button to show the context menu and create nodes.
* Click the **Delete** keyboard button to delete nodes and connections.
* Use scroll to zoom in/out and middle-mouse button to pan the view.

# How to create a custom nodes
To create your own custom node you can simply create new child class of the abstract class **LogicNode** and use it as a template.

In your new class need to define and declare a few things:
1. The name of the node, using the constant **_name** variable and **name** property method.
2. An unique id for the node, using the **_id** variable and the **id** property method (Preferrebly using uuid like the LogicNode class).
3. An empty list where the node can store its connections, using the **_connections** variable and **connections** property method.
4. The UI color of the node, using the **_node_color** variable and **node_color** property method.
5. The input/output, using the **_ports** variable and the **ports** property method. This variable should be a dict. The keys in the dict should be a name string of the ports and the values should be an instance of the **LogicPort** class.
6. Lastly, you also need to define a **node_operation** method which should hold the actual expression or action of the node and then pass that data to the output port. For example, a multiply expression node would have the **node_operation** look something like this:
> output_port.data = (input1_port.data + input2_port.data)

Here is an example on how you can create your own expression node:

```python
import uuid
from core.logic_port import LogicPort

class ExampleNode(LogicNode):

    NAME = None # Name of the node displayed in the UI.

    def __int__(self):
        self.id = uuid.uuid4() # The node need an unique id for save/load functionality to work
        self.node_color = (255, 255, 255) # Color of the node displayed in the UI.
        self.io_ports: = {} # The ports of the node.
        self.connections = [] # All connected nodes will be added here, to determine evaluation order of the nodes.

        # Declare io ports by adding a dict with name keys and instances of LogicPort as values.
        self.io_ports = {"Input" : LogicPort(is_input=True), "Output" : LogicPort(is_input=False)}

    @abstractmethod
    def update(self):
        ''' 
        This method can be used to trigger the node operation externally.
        '''
        return self._node_operation()

    @abstractmethod
    def _node_operation(self):
        ''' 
        This is where the node operation is done.
        For example, a math node would do the calculations here
        before the data is sent to the ouput.
        '''
        pass

```

To make the custom node show up in the scene in the application you need to call the **create_node** method of the controller class.

```python
controller = Controller(scene)
controller.create_node("ExampleNode")
```

The example nodes in the applications are created by connecting the create_node method to a context menu action. Like this:

```python
self.controller.scene.add_contextmenu_item(partial(self.controller.create_node, "AddNode"), "Add Node")
```







