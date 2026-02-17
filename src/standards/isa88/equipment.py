"""ISA-88 Equipment hierarchy."""


class ControlModule:
    def __init__(self, id, type_="Analog"):
        self.id = id
        self.type = type_
        self.io_tags = []

class EquipmentModule:
    def __init__(self, id, type_="Pump"):
        self.id = id
        self.type = type_
        self.control_modules = []

class Unit:
    def __init__(self, id):
        self.id = id
        self.equipment_modules = []
        self.state = "Idle"
        self.allocated_to = None

class ProcessCell:
    def __init__(self, id):
        self.id = id
        self.units = []
