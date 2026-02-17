"""Tests for KonomiSystem."""
import numpy as np
from src.core.system import KonomiSystem


def test_create():
    ks = KonomiSystem(cores=2)
    assert ks.evgpu.cores == 2


def test_block_array():
    ks = KonomiSystem()
    ba = ks.create_block_array("test", (5, 5, 5))
    ba.set(0, 0, 0, 1.0)
    assert ba.get(0, 0, 0) == 1.0
    assert "test" in ks.status()["arrays"]


def test_cube():
    ks = KonomiSystem()
    c = ks.create_cube("c1")
    assert c.id == "c1"
    assert "c1" in ks.status()["cubes"]


def test_evgpu_integration():
    ks = KonomiSystem()
    a = np.eye(4)
    b = np.random.randn(4, 4)
    result = ks.evgpu.tensor(a, b, "@")
    assert np.allclose(result, b)
