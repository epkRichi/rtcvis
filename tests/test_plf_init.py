from rtcvis.plf import Point, PLF
import pytest

def test_1():
    # check that these don't raise any exceptions
    PLF([])
    PLF([Point(0, 0)])
    PLF([Point(0.1, 0), Point(1, 1)])
    PLF([Point(-0.1, 0), Point(1, 1)])
    # points have to be given in the correct order
    with pytest.raises(AssertionError):
        PLF([Point(1, 0), Point(0, 0)])
