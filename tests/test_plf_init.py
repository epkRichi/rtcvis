from rtcvis.plf import Point, PLF
import pytest

def test_1():
    with pytest.raises(AssertionError):
        PLF([])
    with pytest.raises(AssertionError):
        PLF([Point(0, 0)])
    with pytest.raises(AssertionError):
        PLF([Point(1, 0), Point(0, 0)])
    with pytest.raises(AssertionError):
        PLF([Point(0.1, 0), Point(1, 1)])
