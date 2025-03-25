from rtcvis.plf import Point, PLF


def test_1():
    a = PLF([Point(0, 0), Point(2, 2)])
    b = PLF([Point(0, 0), Point(1, 0.5), Point(2, 2.5)])
    assert a - b == PLF([Point(0, 0), Point(1, 0.5), Point(2, -0.5)])


def test_2():
    a = PLF([Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 1)])
    b = PLF([Point(0, 1), Point(2, 3)])
    assert a - b == PLF([Point(0, -1), Point(1, -1), Point(1, -2), Point(2, -2)])


def test_3():
    a = PLF([Point(0, 1), Point(4, 5), Point(8, 4)])
    b = PLF([Point(0, 2), Point(2, 0), Point(5, 1), Point(8, -2)])
    assert a - b == PLF(
        [Point(0, -1), Point(2, 3), Point(4, 5 - 2 / 3), Point(5, 3.75), Point(8, 6)]
    )


def test_4():
    a = PLF([Point(0, 2), Point(2, 0), Point(5, 1), Point(8, -2)])
    assert a - a == PLF([Point(0, 0), Point(2, 0), Point(5, 0), Point(8, 0)])


def test_5():
    a = PLF([Point(-1, 0), Point(1, 2)])
    b = PLF([Point(-1, 0), Point(0, 0), Point(0, 1), Point(1, 1)])
    assert a - b == PLF([Point(-1, 0), Point(0, 1), Point(0, 0), Point(1, 1)])
