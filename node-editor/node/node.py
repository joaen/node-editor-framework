from abc import ABC, abstractmethod

class Node(ABC):
    NAME = None

    def __int__(self):
        self.exsists = True # Should be set to true when instantiated
        self.connections = {}
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()

    @abstractmethod
    def _create_inputs(self):
        ''' 
        This is where the input ports are created and
        then added to the input_ports_dict.
        '''
        return {}
    
    @abstractmethod
    def _create_outputs(self):
        ''' 
        This is where the input ports are created and
        then added to the input_ports_dict.
        '''
        return {}

    @abstractmethod
    def _update_connections(self):
        pass

    @abstractmethod
    def _node_operation(self):
        ''' 
        This is where the node operation is done.
        For example, a math node would do the calculations here
        before the data is sent to the ouput.
        '''
        self._update_connections()
        pass

    @abstractmethod
    def output(self):
        self._node_operation()
        return None
