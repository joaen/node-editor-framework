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
You start the application by running main.py. Make sure the dependencies have been installed first.

# How to create a custom nodes
To create your own custom node you can easily create new child class of the abstract class **LogicNode** and use it as a template.

In your new class need to define the name of your node and define the input and ouput ports of the node by creating instances of the **LogicPort** class. 

You also need to create a node_operation method which is the expression or action of the node. For example, a multiply expression node would have the node_operation look something like this:
> output_port.data = (input1_port.data + input2_port.data)

Here is an example on how you can create your own expression node:

```python
from core.logic_port import LogicPort
from core.logic_node import LogicNode

class ExampleNode(LogicNode):

    NAME = "Example Node"

    def __init__(self):
        self.default_value = 0.0
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()

    def _node_operation(self):
        '''
        Write the actual node expression here
        Eg. output_port.data = (input1_port.data + input2_port.data)
        '''
    
    def update(self):
        '''
        This method is used to update the node externally
        '''
        self._node_operation()
    
    def _create_inputs(self):
        '''
        Create inputs using the LogicPort class
        '''
        input_port = LogicPort(is_input=True, parent_node=self)
        return {"Input" : input_port}
    
    def _create_outputs(self):
        '''
        Create inputs using the LogicPort class
        '''
        ourtput_port = LogicPort(is_input=False, parent_node=self)
        return {"Output" : output_port}

```

To make the node show up in the application you need to pass an instance of your logic node to the create_ui_node method which exsists within the **GraphicsNode** class.
The easiest approach is to create a new context menu item, create new a method where you create the logic node and graphics node, and then connect that context menu item action to your method.

# List of Features





