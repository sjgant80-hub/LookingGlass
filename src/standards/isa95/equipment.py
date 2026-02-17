"""ISA-95 Equipment model."""
from enum import Enum


class EquipmentState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    FAULTED = "faulted"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"

class EquipmentMode(Enum):
    PRODUCTION = "production"
    MAINTENANCE = "maintenance"
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SEMIAUTO = "semiauto"

class Equipment:
    def __init__(self, id, name, level=None):
        self.id = id
        self.name = name
        self.level = level
        self.state = EquipmentState.IDLE
        self.mode = EquipmentMode.AUTOMATIC
        self.children = []
        self.capabilities = []
