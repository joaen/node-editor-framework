from abc import ABC, abstractmethod

class Node(ABC):
    def __int__(self):
        self._create_inputs()
        self._create_outputs()

    @property
    @abstractmethod
    def exsist(self) -> bool:
        pass

    @abstractmethod
    def _create_inputs(self):
        pass
    
    @abstractmethod
    def _create_outputs(self):
       pass

    @abstractmethod
    def _update_connections(self):
        pass

    @abstractmethod
    def _node_operation(self):
        ''' 
        This is where the node operation is done.
        For exmaple, a math node would do the calculations here
        before the data is sent to the ouput.
        '''
        self._update_connections()
        pass

    @abstractmethod
    def output(self):
        self._node_operation()
        return None
