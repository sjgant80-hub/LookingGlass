"""ISA-95 Production scheduling and performance."""


class ProcessSegment:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.equipment = []
        self.materials_in = []
        self.materials_out = []
        self.params = {}

class ProductionSchedule:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end
        self.segments = []
        self.priority = 0
        self.state = "created"

class ProductionPerformance:
    def __init__(self, schedule_ref):
        self.schedule_ref = schedule_ref
        self.actual_start = None
        self.actual_end = None
        self.kpis = {}
