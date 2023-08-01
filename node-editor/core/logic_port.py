
class LogicPort():

    def __init__(self, is_input=True, parent_node=None, name=None, data=None):
        self.name = name
        self._data = data
        self.parent_node = parent_node
        self.connection : LogicPort = None
        self.is_connected = False
        self.is_input = is_input

    @property
    def data(self):
        if self.is_connected and self.is_input:

            return self.connection.data
        else:
            return self._data
    
    @data.setter
    def data(self, value):
        self._data = value


    
