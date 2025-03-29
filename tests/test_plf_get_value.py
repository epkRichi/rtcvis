from rtcvis import *
import pytest


def test_1():
    with pytest.raises(AssertionError):
        PLF([]).get_value(0)
    with pytest.raises(AssertionError):
        PLF([(-1, 0)]).get_value(0)
    with pytest.raises(AssertionError):
        PLF([(1, 0)]).get_value(0)


def test_2():
    assert PLF([(5, 3)]).get_value(5) == 3
    a = PLF([(-1, 0), (0, 1), (1, -1)])
    assert a.get_value(-1) == 0
    assert a.get_value(-0.5) == 0.5
    assert a.get_value(-0.1) == 0.9
    assert a.get_value(0) == 1
    assert a.get_value(0.5) == 0
    assert a.get_value(0.75) == -0.5
    assert a.get_value(1) == -1
