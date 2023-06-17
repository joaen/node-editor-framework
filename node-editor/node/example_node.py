from node.port import Port
# from node.node import Node

class ExampleNode():

    NAME = "Example Node"

    def __init__(self):
        # self.input_ports_dict = dict()
        # self.output_ports_dict = dict()
        self.connections = dict()
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()

    def _create_inputs(self):
        self.input_port_1 = Port()
        self.input_port_2 = Port()

        inputs_dict = {}
        inputs_dict["input_port_1"] = self.input_port_1
        inputs_dict["input_port_2"] = self.input_port_2
        return inputs_dict
    
    def _create_outputs(self):
        self.output_port_1 = Port(is_input=False)
        self.output_port_2 = Port(is_input=False)

        outputs_dict = {}
        outputs_dict["output_port_1"] = self.output_port_1
        outputs_dict["output_port_2"] = self.output_port_2
        return outputs_dict

    @property
    def output_1(self):
        self.output_port_1.data = (self.input_port_1.data * self.input_port_2.data)
        return self.output_port_1.data
    
    @property
    def output_2(self):
        self.output_port_2.data = (self.input_port_1.data + self.input_port_2.data)
        return self.output_port_2.data

