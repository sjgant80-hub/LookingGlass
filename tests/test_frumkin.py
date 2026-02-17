"""Tests for Frumkin model."""
import math
from src.enterprise.frumkin import FrumkinModel, PHI, PHI_INV


def test_phi():
    assert abs(PHI - 1.618033988) < 1e-6
    assert abs(PHI_INV - 0.618033988) < 1e-6


def test_equilibrium():
    m = FrumkinModel()
    assert abs(m.equilibrium() - PHI_INV) < 1e-10


def test_health():
    m = FrumkinModel()
    h = m.health(PHI_INV)
    assert abs(h - 1.0) < 1e-10
    h2 = m.health(0.0)
    assert h2 < 0.5


def test_predict():
    m = FrumkinModel()
    assert m.predict_stability(0.08) == "terminal"
    assert m.predict_stability(0.32) == "critical"
    assert m.predict_stability(0.52) == "unstable"
    assert m.predict_stability(0.61) == "stable"
    assert m.predict_stability(0.68) == "robust"
