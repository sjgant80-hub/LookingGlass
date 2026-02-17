"""FemtoLLM - 16-dim nano language model."""
import numpy as np


class FemtoLLM:
    """Minimal LLM: 16 hidden dims, 4MB RAM."""

    H = 16

    def __init__(self):
        self.W = np.random.randn(self.H, self.H) * 0.1
        self.b = np.zeros(self.H)

    def encode(self, text):
        v = np.zeros(self.H)
        for i, c in enumerate(text[: self.H]):
            v[i] = ord(c) / 128.0
        return v

    def forward(self, x):
        return np.tanh(self.W @ x + self.b)

    async def process(self, text):
        x = self.encode(text)
        y = self.forward(x)
        return {"input": text[:50], "embedding": y.tolist()}
