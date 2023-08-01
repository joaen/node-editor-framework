from abc import ABC, abstractmethod
import uuid

class LogicNode(ABC):

    NAME = None

    def __int__(self):
        self._id = uuid.uuid4() # The node need an unique id for save/load functionality to work
        self.node_color = (255, 255, 255)
        self.input_ports = self._create_inputs()
        self.output_ports = self._create_outputs()
        self.connections = []

    @abstractmethod
    def _create_inputs(self):
        ''' 
        This is where the input LogicPort instances are created and
        then added to the input_ports.
        '''
        return {}
    
    @abstractmethod
    def _create_outputs(self):
        ''' 
        This is where the output LogicPort instances are created and
        then added to the output_ports.
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

    @property
    @abstractmethod
    def id(self):
        return self._id

    @id.setter
    @abstractmethod
    def id(self, new_id):
        self._id = new_id

