"""OPC-UA Node model."""
from enum import Enum


class NodeClass(Enum):
    OBJECT = "Object"
    VARIABLE = "Variable"
    METHOD = "Method"
    VIEW = "View"
    DATA_TYPE = "DataType"

class Node:
    def __init__(self, node_id, name, node_class):
        self.node_id = node_id
        self.browse_name = name
        self.display_name = name
        self.node_class = node_class
        self.parent = None
        self.children = []

class Variable(Node):
    def __init__(self, node_id, name, data_type="Double"):
        super().__init__(node_id, name, NodeClass.VARIABLE)
        self.data_type = data_type
        self.value = None
        self.access = "RW"
        self.historizing = False

class Method(Node):
    def __init__(self, node_id, name):
        super().__init__(node_id, name, NodeClass.METHOD)
        self.input_args = []
        self.output_args = []
