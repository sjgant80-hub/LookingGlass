"""ISA-95 Levels L0-L4."""
from enum import Enum


class ISA95Level(Enum):
    L0 = ("Process", "Physical", "continuous")
    L1 = ("Sensing", "Direct Control", "ms-sec")
    L2 = ("Control", "Supervision", "sec-hours")
    L3 = ("MOM", "MES/Execution", "shifts-days")
    L4 = ("Business", "Planning/ERP", "days-months")

    def __init__(self, label, scope, timescale):
        self.label = label
        self.scope = scope
        self.timescale = timescale

HIERARCHY = [
    "Enterprise", "Site", "Area",
    "WorkCenter", "WorkUnit", "Equipment",
]
