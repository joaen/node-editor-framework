# Python + PySide2 Node Editor
Node editor framework which can be used as a standalone application or integrated into Python + PySide2 projects.

 ![image](https://github.com/joaen/node-editor-framework/assets/6629861/9a3bac56-ef48-40a8-bf78-44a5ae5ee893)

 # Dependencies
* PySide2==5.15.2.1
* shiboken2==5.15.2.1

To install the dependencies in your current environment you can run the following snippet:
```
pip install -r requirements.txt
```
# How to run
You start the application by running main.py. Make sure the depdencies have been installed first.

# How to create custom nodes
To create a custom node you can create a new class child class of LogicNode. 
There you can set the name of the node and declare the input and ouput ports of the node.
You also need to create a node_operation method where the actual expression is run. For exmaple inside the exmaple AddNode the node_operation module is:
> output_port.data = (input1_port.data + input2_port.data)

To make the node show up in the application you need to pass an instance of your logic node to the create_ui_node method which exsists within the GraphicsNode class.
The easiest approach is to create new a method to create your custom node and then create new context menu item in the scene and connect that menu item action to your method.

```python
from core.logic_port import LogicPort
from core.logic_node import LogicNode

class ExampleNode(LogicNode):

    NAME = "Example Node"

    def __init__(self):
        self.exsists = True
        self.default_value = 0.0
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()

    def _node_operation(self):
        '''
        Write the actual node expression here
        '''
    
    def update(self):
        '''
         Update the node externally using this method
         '''
        self._node_operation()
    
    def _create_inputs(self):
        input_port = LogicPort(is_input=True, parent_node=self)
        return {"Input" : input_port}
    
    def _create_outputs(self):
        ourtput_port = LogicPort(is_input=False, parent_node=self)
        return {"Output" : output_port}

```
# List of Features



