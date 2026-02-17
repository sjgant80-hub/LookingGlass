"""ISA-101 Graphic elements and faceplates."""


class GraphicElement:
    def __init__(self, id, type_, tags=None):
        self.id = id
        self.type = type_
        self.tags = tags or {}
        self.states = []

class Faceplate:
    def __init__(self, equipment_ref, title):
        self.equipment = equipment_ref
        self.title = title
        self.pv_display = []
        self.sp_input = []
        self.commands = []
        self.status = {}

class Trend:
    def __init__(self, tags, timespan, sample_rate):
        self.tags = tags
        self.timespan = timespan
        self.sample_rate = sample_rate
