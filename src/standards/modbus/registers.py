"""Modbus register types."""
from enum import Enum


class RegisterType(Enum):
    COIL = ("Coil", "RW", "bit", 1, 5)
    DISCRETE_INPUT = ("DI", "RO", "bit", 2, None)
    HOLDING = ("HR", "RW", "uint16", 3, 6)
    INPUT = ("IR", "RO", "uint16", 4, None)

    def __init__(self, label, access, dtype, fc_r, fc_w):
        self.label = label
        self.access = access
        self.dtype = dtype
        self.fc_read = fc_r
        self.fc_write = fc_w


class ModbusMap:
    def __init__(self):
        self.entries = []

    def add(self, tag, unit_id, reg_type, addr, data_type):
        self.entries.append({
            "tag": tag, "unit_id": unit_id,
            "register": reg_type, "addr": addr,
            "data_type": data_type,
        })
