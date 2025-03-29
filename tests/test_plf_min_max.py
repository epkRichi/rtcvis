from rtcvis import *


def test_1():
    assert PLF([(0, 0), (1, 1)]).min == 0
    assert PLF([(0, 0), (1, 1)]).max == 1
    assert PLF([(-5, -1), (1, 1), (1, -1.5), (30, 1.1)]).min == -1.5
    assert PLF([(-5, -1), (1, 1), (1, -1.5), (30, 1.1)]).max == 1.1
