"""Tests for eVGPU."""
import numpy as np
from src.core.evgpu import eVGPU


def test_matmul():
    gpu = eVGPU(cores=2)
    a = np.eye(3)
    b = np.ones((3, 3))
    result = gpu.tensor(a, b, "@")
    assert result.shape == (3, 3)
    assert np.allclose(result, b)


def test_add():
    gpu = eVGPU()
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    result = gpu.tensor(a, b, "+")
    assert np.array_equal(result, [5, 7, 9])


def test_activate_relu():
    gpu = eVGPU()
    x = np.array([-1, 0, 1, 2])
    result = gpu.activate(x, "relu")
    assert np.array_equal(result, [0, 0, 1, 2])


def test_activate_sigmoid():
    gpu = eVGPU()
    result = gpu.activate(np.array([0.0]), "sigmoid")
    assert abs(result[0] - 0.5) < 1e-6
