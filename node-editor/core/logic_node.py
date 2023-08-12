from abc import ABC, abstractmethod
import uuid
from core.logic_port import LogicPort

class LogicNode(ABC):

    NAME = None # Name of the node displayed in the UI.

    def __int__(self):
        self.id = uuid.uuid4() # The node need an unique id for save/load functionality to work
        self.node_color = (255, 255, 255) # Color of the node displayed in the UI.
        self.io_ports: {str, LogicPort} = {} # The ports of the node.
        self.connections = [] # All connected nodes will be added here, to determine evaluation order of the nodes.

    @abstractmethod
    def execute(self):
        ''' 
        This is where the node operation is done.
        For example, a math node would do the calculations here
        before the data is sent to the ouput.
        '''
        pass