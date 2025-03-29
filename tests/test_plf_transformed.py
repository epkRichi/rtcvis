from rtcvis import *


def test_1():
    f = PLF([(0, 0), (1, 1)])
    assert f.transformed(True, 1) == PLF([(0, 1), (1, 0)])


def test_2():
    f = PLF([(0, 0), (1, 1)])
    assert f.transformed(False, -0.5) == PLF([(-0.5, 0), (0.5, 1)])


def test_3():
    f = PLF([(0, 0), (1, 1)])
    assert f.transformed(True, 0.5) == PLF([(-0.5, 1), (0.5, 0)])


def test_4():
    f = PLF([(0, 1), (1, 1)])
    assert f.transformed(True, 0.5) == PLF([(-0.5, 1), (0.5, 1)])


def test_5():
    f = PLF([(0, 1), (3, 2.5), (4, 3), (8, 4)])
    assert f.transformed(True, 3.5) == PLF([(-4.5, 4), (-0.5, 3), (0.5, 2.5), (3.5, 1)])
