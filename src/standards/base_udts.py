"""Layer 1: Base UDTs shared by all standards."""
from enum import IntEnum


class Quality(IntEnum):
    BAD = 0
    UNCERTAIN = 64
    GOOD = 192

class Severity:
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    FATAL = "fatal"

class Value:
    """Tagged value with quality and timestamp."""
    def __init__(self, v, quality=Quality.GOOD, ts=None, unit=None):
        self.v = v
        self.q = quality
        self.t = ts
        self.unit = unit

class Range:
    def __init__(self, lo, hi, unit=None):
        self.lo = lo
        self.hi = hi
        self.unit = unit

    def contains(self, v):
        return self.lo <= v <= self.hi

class Duration:
    def __init__(self, value, unit="s"):
        self.value = value
        self.unit = unit
