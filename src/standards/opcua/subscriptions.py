"""OPC-UA Subscriptions and monitored items."""


class MonitoredItem:
    def __init__(self, id, node_ref, interval_ms=1000):
        self.id = id
        self.node = node_ref
        self.sampling_interval = interval_ms
        self.queue_size = 10
        self.discard_oldest = True

class Subscription:
    def __init__(self, id, interval_ms=1000):
        self.id = id
        self.publishing_interval = interval_ms
        self.enabled = True
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def item_count(self):
        return len(self.items)
