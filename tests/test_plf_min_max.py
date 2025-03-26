from rtcvis import *


def test_1():
    assert PLF([Point(0, 0), Point(1, 1)]).min == 0
    assert PLF([Point(0, 0), Point(1, 1)]).max == 1
    assert PLF([Point(-5, -1), Point(1, 1), Point(1, -1.5), Point(30, 1.1)]).min == -1.5
    assert PLF([Point(-5, -1), Point(1, 1), Point(1, -1.5), Point(30, 1.1)]).max == 1.1
