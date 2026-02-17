"""ISA-88 Recipe model."""


class Phase:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.params = []
        self.state = "IDLE"

class Operation:
    def __init__(self, id, phases=None):
        self.id = id
        self.phases = phases or []

class UnitProcedure:
    def __init__(self, id, operations=None):
        self.id = id
        self.operations = operations or []

class Recipe:
    def __init__(self, id, name, product):
        self.id = id
        self.name = name
        self.product = product
        self.level = "Master"
        self.procedures = []
        self.formula = {"inputs": [], "outputs": []}
