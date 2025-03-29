from rtcvis import *
import pytest


def test_1():
    # check that these don't raise any exceptions
    PLF([])
    PLF([(0, 0)])
    PLF([(0.1, 0), (1, 1)])
    PLF([(-0.1, 0), (1, 1)])
    PLF([(-1, 0), (0.5, 1), (0.5, 2), (2, 0)])
    PLF([(-1, 0), (0.5, 1), (0.5, 1), (2, 0)])
    PLF([(1, 1), (1, 2)])
    PLF([(1, 1), (1, 1)])
    # these should raise exceptions
    with pytest.raises(AssertionError):
        PLF([(1, 0), (0, 0)])
    with pytest.raises(AssertionError):
        PLF([(-1, 0), (0.5, 1), (0.5, 2), (0.5, 3), (2, 0)])
