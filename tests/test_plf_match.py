from rtcvis import *
from rtcvis.plf import match_plf


def test_1():
    a = PLF([Point(0, 0), Point(2, 2)])
    b = PLF([Point(0, 0), Point(1, 0.5), Point(2, 2.5)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([Point(0, 0), Point(1, 1), Point(2, 2)])
    assert new_b == b


def test_2():
    a = PLF([Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 1)])
    b = PLF([Point(0, 1), Point(2, 3)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == PLF([Point(0, 1), Point(1, 2), Point(1, 2), Point(2, 3)])


def test_3():
    a = PLF([Point(0, 1), Point(4, 5), Point(8, 4)])
    b = PLF([Point(0, 2), Point(2, 0), Point(5, 1), Point(8, -2)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF(
        [Point(0, 1), Point(2, 3), Point(4, 5), Point(5, 4.75), Point(8, 4)]
    )
    assert new_b == PLF(
        [Point(0, 2), Point(2, 0), Point(4, 2 / 3), Point(5, 1), Point(8, -2)]
    )


def test_4():
    a = PLF([Point(0, 2), Point(2, 0), Point(5, 1), Point(8, -2)])
    new_a_1, new_a_2 = match_plf(a, a)
    assert new_a_1 == a
    assert new_a_2 == a


def test_5():
    a = PLF([])
    b = PLF([Point(0, 0)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == a


def test_6():
    a = PLF([])
    new_a_1, new_a_2 = match_plf(a, a)
    assert new_a_1 == a
    assert new_a_2 == a


def test_7():
    a = PLF([Point(3, -1)])
    b = PLF([Point(-2, 5)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([])
    assert new_b == PLF([])


def test_8():
    a = PLF([Point(-2, -1)])
    b = PLF([Point(-2, 5)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == b


def test_9():
    a = PLF([Point(-2, -1)])
    b = PLF([Point(-3, 5), Point(-1, 6)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == PLF([Point(-2, 5.5)])


def test_10():
    a = PLF([Point(-1, 0), Point(1, 0)])
    b = PLF([Point(-2, 1), Point(0, 0), Point(2, 1)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([Point(-1, 0), Point(0, 0), Point(1, 0)])
    assert new_b == PLF([Point(-1, 0.5), Point(0, 0), Point(1, 0.5)])


def test_11():
    a = PLF([Point(-1, 0), Point(0, 0), Point(0, 1), Point(1, 1)])
    b = PLF([Point(-0.5, 0), Point(1.5, 2)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([Point(-0.5, 0), Point(0, 0), Point(0, 1), Point(1, 1)])
    assert new_b == PLF([Point(-0.5, 0), Point(0, 0.5), Point(0, 0.5), Point(1, 1.5)])
