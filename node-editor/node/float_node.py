from node.port import Port
from node.node import Node

class FloatNode(Node):

    NAME = "Float Node"

    def __init__(self, number=0):
        super().__init__()
        self.connections = None
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()
        self.output_port.data = number

    @property
    def exsist(self) -> bool:
        return super().exsist

    def _node_operation(self):
        return super()._node_operation()
    
    def _update_connections(self):
        return super()._update_connections()
    
    def _create_inputs(self):
        return super()._create_inputs()
    
    def _create_outputs(self):
        self.output_port = Port(is_input=False, parent_node=self)
        output_dict = {"ouput_lala" : self.output_port}
        return output_dict

    def output(self):
        return super().output()



