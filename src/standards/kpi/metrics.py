"""KPI metric models."""


class MTBF:
    """Mean Time Between Failures."""
    def __init__(self, uptime_hrs=0, failures=0):
        self.uptime = uptime_hrs
        self.failures = failures

    @property
    def value(self):
        return self.uptime / self.failures if self.failures else float("inf")

class CycleTime:
    def __init__(self, ideal, actual):
        self.ideal = ideal
        self.actual = actual

    @property
    def efficiency(self):
        return self.ideal / self.actual if self.actual else 0

class Throughput:
    def __init__(self, units, hours):
        self.units = units
        self.hours = hours

    @property
    def rate(self):
        return self.units / self.hours if self.hours else 0
