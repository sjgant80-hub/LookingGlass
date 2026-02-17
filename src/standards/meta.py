"""Layer 0: Meta-Standard - how standards are defined."""


class UDT:
    """User Defined Type base."""
    def __init__(self, name, base=None, fields=None):
        self.name = name
        self.base = base
        self.fields = fields or []

class Level:
    """Hierarchy level definition."""
    def __init__(self, id, name, scope, timescale=""):
        self.id = id
        self.name = name
        self.scope = scope
        self.timescale = timescale

class StateMachine:
    """State model with transitions."""
    def __init__(self, name, states, initial):
        self.name = name
        self.states = states
        self.initial = initial
        self.transitions = []

    def add(self, frm, to, trigger):
        self.transitions.append(
            {"from": frm, "to": to, "trigger": trigger}
        )

class Standard:
    """Top-level standard container."""
    def __init__(self, id, scope):
        self.id = id
        self.scope = scope
        self.udts = []
        self.hierarchy = []
        self.states = []
