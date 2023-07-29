
class LogicPort():

    def __init__(self, is_input=True, parent_node=None, name=None):
        self.name = name
        self._data = 0
        self.parent_node = parent_node
        self.connection : LogicPort = None
        self.is_connected = False
        self.is_input = is_input

    def set_data(self, data):
        self.data = data

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value


    
