"""Tests for standards modules."""
from src.standards.base_udts import Quality, Value, Range
from src.standards.kpi.oee import OEE
from src.standards.crosswalks import crosswalk


def test_quality():
    assert Quality.GOOD == 192
    assert Quality.BAD == 0


def test_value():
    v = Value(42.0, Quality.GOOD, unit="degC")
    assert v.v == 42.0
    assert v.q == Quality.GOOD


def test_range():
    r = Range(0, 100, "psi")
    assert r.contains(50)
    assert not r.contains(101)


def test_oee():
    o = OEE()
    o.run_time = 90
    o.downtime = 10
    o.actual_rate = 95
    o.ideal_rate = 100
    o.good_units = 99
    o.total_units = 100
    assert abs(o.availability - 0.9) < 0.01
    assert abs(o.value - 0.846) < 0.01


def test_crosswalk():
    r = crosswalk("WorkCenter", "ISA95", "ISA88")
    assert r == "ProcessCell"
