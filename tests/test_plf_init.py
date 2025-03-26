from rtcvis import *
import pytest


def test_1():
    # check that these don't raise any exceptions
    PLF([])
    PLF([Point(0, 0)])
    PLF([Point(0.1, 0), Point(1, 1)])
    PLF([Point(-0.1, 0), Point(1, 1)])
    PLF([Point(-1, 0), Point(0.5, 1), Point(0.5, 2), Point(2, 0)])
    PLF([Point(-1, 0), Point(0.5, 1), Point(0.5, 1), Point(2, 0)])
    PLF([Point(1, 1), Point(1, 2)])
    PLF([Point(1, 1), Point(1, 1)])
    # these should raise exceptions
    with pytest.raises(AssertionError):
        PLF([Point(1, 0), Point(0, 0)])
    with pytest.raises(AssertionError):
        PLF([Point(-1, 0), Point(0.5, 1), Point(0.5, 2), Point(0.5, 3), Point(2, 0)])
