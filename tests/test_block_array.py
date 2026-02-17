"""Tests for BlockArray."""
from src.core.block_array import BlockArray


def test_create():
    ba = BlockArray((5, 5, 5))
    assert ba.dims == (5, 5, 5)
    assert ba.active_count() == 0


def test_set_get():
    ba = BlockArray()
    ba.set(1, 2, 3, 42.0)
    assert ba.get(1, 2, 3) == 42.0
    assert ba.get(0, 0, 0) == 0.0
    assert ba.active_count() == 1


def test_llm_at():
    ba = BlockArray()
    llm = ba.llm_at(0, 0, 0)
    assert llm is not None
    same = ba.llm_at(0, 0, 0)
    assert llm is same
