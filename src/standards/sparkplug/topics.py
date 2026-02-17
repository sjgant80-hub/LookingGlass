"""Sparkplug B topic namespace."""
from enum import IntEnum


class QoS(IntEnum):
    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2

TOPIC_TYPES = [
    "NBIRTH", "NDEATH", "DBIRTH", "DDEATH",
    "NDATA", "DDATA", "NCMD", "DCMD",
]


class SparkplugTopic:
    NS = "spBv1.0"

    def __init__(self, group, edge_node, device=None):
        self.group = group
        self.edge_node = edge_node
        self.device = device

    def topic(self, msg_type):
        base = f"{self.NS}/{self.group}/{msg_type}/{self.edge_node}"
        if self.device and msg_type.startswith("D"):
            return f"{base}/{self.device}"
        return base
