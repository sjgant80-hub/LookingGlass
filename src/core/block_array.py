"""BlockArray - Sparse 3D compute grid."""
import numpy as np
from .femtollm import FemtoLLM


class BlockArray:
    """Sparse 1000^3 grid with LLM at coords."""

    def __init__(self, dims=(10, 10, 10)):
        self.dims = dims
        self.data = {}
        self.llms = {}

    def set(self, x, y, z, value):
        self.data[(x, y, z)] = value

    def get(self, x, y, z):
        return self.data.get((x, y, z), 0.0)

    def llm_at(self, x, y, z):
        key = (x, y, z)
        if key not in self.llms:
            self.llms[key] = FemtoLLM()
        return self.llms[key]

    def active_count(self):
        return len(self.data)
