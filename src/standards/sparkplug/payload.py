"""Sparkplug B payload model."""


class Metric:
    def __init__(self, name, datatype, value):
        self.name = name
        self.datatype = datatype
        self.value = value
        self.alias = None
        self.timestamp = None

class SparkplugPayload:
    def __init__(self, seq=0):
        self.timestamp = None
        self.seq = seq
        self.metrics = []

    def add_metric(self, name, datatype, value):
        m = Metric(name, datatype, value)
        self.metrics.append(m)
        return m

    def next_seq(self):
        self.seq = (self.seq + 1) % 256
        return self.seq
