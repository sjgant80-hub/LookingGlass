"""ISA-18.2 Alarm priorities."""
from enum import IntEnum


class AlarmPriority(IntEnum):
    EMERGENCY = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

PRIORITY_CONFIG = {
    1: {"name": "Emergency", "response": "<1min",
        "color": "Red", "sound": "Continuous"},
    2: {"name": "High", "response": "<10min",
        "color": "Orange", "sound": "Fast"},
    3: {"name": "Medium", "response": "<1hr",
        "color": "Yellow", "sound": "Slow"},
    4: {"name": "Low", "response": "Shift",
        "color": "Cyan", "sound": "None"},
}
