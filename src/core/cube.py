"""Cube - 9-node compute unit (8 vertices + center)."""
from collections import defaultdict
from .femtollm import FemtoLLM


VERTICES = [
    "NEU", "NED", "NWU", "NWD",
    "SEU", "SED", "SWU", "SWD",
]


class Cube:
    """8 vertex LLMs + 1 central coordinator."""

    def __init__(self, cube_id):
        self.id = cube_id
        self.vertices = {v: FemtoLLM() for v in VERTICES}
        self.central = FemtoLLM()
        self.edges = defaultdict(list)

    def connect(self, src, dst):
        self.edges[src].append(dst)
        self.edges[dst].append(src)

    async def process_vertex(self, vertex, text):
        llm = self.vertices.get(vertex, self.central)
        return await llm.process(text)

    def status(self):
        return {
            "id": self.id,
            "vertices": list(self.vertices.keys()),
            "edges": dict(self.edges),
        }
