"""Overall Equipment Effectiveness."""


class OEE:
    """OEE = Availability * Performance * Quality."""

    def __init__(self):
        self.run_time = 0
        self.downtime = 0
        self.actual_rate = 0
        self.ideal_rate = 1
        self.good_units = 0
        self.total_units = 0

    @property
    def availability(self):
        t = self.run_time + self.downtime
        return self.run_time / t if t > 0 else 0

    @property
    def performance(self):
        if self.ideal_rate == 0:
            return 0
        return self.actual_rate / self.ideal_rate

    @property
    def quality(self):
        if self.total_units == 0:
            return 0
        return self.good_units / self.total_units

    @property
    def value(self):
        return self.availability * self.performance * self.quality
