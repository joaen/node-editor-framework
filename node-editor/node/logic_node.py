from abc import ABC, abstractmethod

class LogicNode(ABC):

    NAME = None

    def __int__(self):
        self.exsists = True # Should be set to true when instantiated
        self.node_color = (255, 255, 255)
        self.input_ports_dict = self._create_inputs()
        self.output_ports_dict = self._create_outputs()

    @abstractmethod
    def _create_inputs(self):
        ''' 
        This is where the input LogicPort instances are created and
        then added to the input_ports_dict.
        '''
        return {}
    
    @abstractmethod
    def _create_outputs(self):
        ''' 
        This is where the output LogicPort instances are created and
        then added to the output_ports_dict.
        '''
        return {}

    @abstractmethod
    def update(self):
        ''' 
        This method can be used to trigger the node operation externally.
        '''
        pass

    @abstractmethod
    def _node_operation(self):
        ''' 
        This is where the node operation is done.
        For example, a math node would do the calculations here
        before the data is sent to the ouput.
        '''
        pass

