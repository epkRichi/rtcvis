from rtcvis.plf import Point, PLF


def test_1():
    f = PLF([Point(0, 0), Point(1, 1)])
    assert f.transformed(True, 1) == PLF([Point(0, 1), Point(1, 0)])

def test_2():
    f = PLF([Point(0, 0), Point(1, 1)])
    assert f.transformed(False, -0.5) == PLF([Point(0, 0.5), Point(0.5, 1)])

def test_3():
    f = PLF([Point(0, 0), Point(1, 1)])
    assert f.transformed(True, 0.5) == PLF([Point(0, 0.5), Point(0.5, 0)])

def test_4():
    f = PLF([Point(0, 1), Point(1, 1)])
    assert f.transformed(True, 0.5) == PLF([Point(0, 1), Point(0.5, 1)])

def test_5():
    f = PLF([Point(0, 1), Point(3, 2.5), Point(4, 3), Point(8, 4)])
    assert f.transformed(True, 3.5) == PLF([Point(0, 2.75), Point(0.5, 2.5), Point(3.5, 1)])
    