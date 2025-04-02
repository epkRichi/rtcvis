from rtcvis import *


def test_1():
    assert PLF([(0, 0), (1, 1)]).min == Point(0, 0)
    assert PLF([(0, 0), (1, 1)]).max == Point(1, 1)
    assert PLF([(-5, -1), (1, 1), (1, -1.5), (30, 1.1)]).min == Point(1, -1.5)
    assert PLF([(-5, -1), (1, 1), (1, -1.5), (30, 1.1)]).max == Point(30, 1.1)
