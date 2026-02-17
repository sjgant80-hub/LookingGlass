"""Tests for Cube."""
import asyncio
from src.core.cube import Cube, VERTICES


def test_create():
    c = Cube("test-1")
    assert c.id == "test-1"
    assert len(c.vertices) == 8


def test_connect():
    c = Cube("c1")
    c.connect("NEU", "SWD")
    assert "SWD" in c.edges["NEU"]
    assert "NEU" in c.edges["SWD"]


def test_status():
    c = Cube("c1")
    s = c.status()
    assert s["id"] == "c1"
    assert len(s["vertices"]) == 8


def test_process():
    c = Cube("c1")
    result = asyncio.run(c.process_vertex("NEU", "hello"))
    assert "input" in result
