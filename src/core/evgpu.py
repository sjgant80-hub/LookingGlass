"""eVGPU - Electronic Virtual GPU. Pure CPU AI/ML."""
import numpy as np


class eVGPU:
    """CPU-based tensor operations. No GPU needed."""

    def __init__(self, cores=4):
        self.cores = cores

    def matmul(self, a, b):
        return np.matmul(a, b)

    def add(self, a, b):
        return np.add(a, b)

    def tensor(self, a, b, op="@"):
        ops = {"@": self.matmul, "+": self.add}
        return ops.get(op, self.matmul)(a, b)

    def activate(self, x, fn="relu"):
        if fn == "relu":
            return np.maximum(0, x)
        if fn == "sigmoid":
            return 1 / (1 + np.exp(-x))
        return np.tanh(x)
