"""Tests for FemtoLLM."""
import asyncio
import numpy as np
from src.core.femtollm import FemtoLLM


def test_encode():
    llm = FemtoLLM()
    v = llm.encode("Hello")
    assert len(v) == 16
    assert v[0] == ord("H") / 128.0


def test_forward():
    llm = FemtoLLM()
    x = np.ones(16) * 0.5
    y = llm.forward(x)
    assert y.shape == (16,)
    assert all(-1 <= yi <= 1 for yi in y)


def test_process():
    llm = FemtoLLM()
    result = asyncio.run(llm.process("test input"))
    assert "input" in result
    assert "embedding" in result
    assert len(result["embedding"]) == 16
