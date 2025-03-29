from rtcvis import *


def test_start_1():
    f = PLF([(0, 0), (1, 1)])
    assert f.start_truncated(0) == f


def test_start_2():
    f = PLF([(0, 0), (1, 1)])
    assert f.start_truncated(-0.5) == f


def test_start_3():
    f = PLF([(0, 0), (1, 1)])
    assert f.start_truncated(0.2) == PLF([(0.2, 0.2), (1, 1)])


def test_start_4():
    f = PLF([(0, 0), (1, 1)])
    assert f.start_truncated(1) == PLF([(1, 1)])


def test_start_5():
    f = PLF([(0, 0), (1, 1)])
    assert f.start_truncated(1.1) == PLF([])


def test_end_1():
    f = PLF([(0, 0), (1, 1)])
    assert f.end_truncated(0) == PLF([(0, 0)])


def test_end_2():
    f = PLF([(0, 0), (1, 1)])
    assert f.end_truncated(-0.5) == PLF([])


def test_end_3():
    f = PLF([(0, 0), (1, 1)])
    assert f.end_truncated(0.2) == PLF([(0, 0), (0.2, 0.2)])


def test_end_4():
    f = PLF([(0, 0), (1, 1)])
    assert f.end_truncated(1) == f


def test_end_5():
    f = PLF([(0, 0), (1, 1)])
    assert f.end_truncated(1.1) == f
