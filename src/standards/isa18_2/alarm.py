"""ISA-18.2 Alarm model."""
from enum import Enum


class AlarmState(Enum):
    NORMAL = "normal"
    UNACKED = "unacked"
    ACKED = "acked"
    RTN_UNACK = "rtn_unack"
    SHELVED = "shelved"
    OUT_OF_SERVICE = "oos"

class Alarm:
    def __init__(self, id, tag, type_, priority=3):
        self.id = id
        self.tag = tag
        self.type = type_
        self.priority = priority
        self.state = AlarmState.NORMAL
        self.message = ""
        self.consequence = ""
        self.response = ""

    def activate(self):
        self.state = AlarmState.UNACKED

    def acknowledge(self):
        if self.state == AlarmState.UNACKED:
            self.state = AlarmState.ACKED

    def clear(self):
        if self.state == AlarmState.ACKED:
            self.state = AlarmState.NORMAL
        elif self.state == AlarmState.UNACKED:
            self.state = AlarmState.RTN_UNACK
