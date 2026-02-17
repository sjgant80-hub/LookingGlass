"""ISA-88 Batch model."""


class Batch:
    def __init__(self, id, recipe_ref):
        self.id = id
        self.recipe_ref = recipe_ref
        self.state = "Created"
        self.start = None
        self.end = None
        self.unit_allocs = []
        self.events = []
        self.params = {}

    def start_batch(self, timestamp):
        self.state = "Running"
        self.start = timestamp

    def complete(self, timestamp):
        self.state = "Complete"
        self.end = timestamp

    def abort(self):
        self.state = "Aborted"
