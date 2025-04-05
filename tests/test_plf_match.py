from rtcvis import *
from rtcvis.plf import match_plf


def test_1():
    a = PLF([(0, 0), (2, 2)])
    b = PLF([(0, 0), (1, 0.5), (2, 2.5)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 0), (1, 1), (2, 2)])
    assert new_b == b


def test_2():
    a = PLF([(0, 0), (1, 1), (1, 0), (2, 1)])
    b = PLF([(0, 1), (2, 3)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == PLF([(0, 1), (1, 2), (1, 2), (2, 3)])


def test_3():
    a = PLF([(0, 1), (4, 5), (8, 4)])
    b = PLF([(0, 2), (2, 0), (5, 1), (8, -2)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 1), (2, 3), (4, 5), (5, 4.75), (8, 4)])
    assert new_b == PLF([(0, 2), (2, 0), Point(4, 2 / 3), (5, 1), (8, -2)])


def test_4():
    a = PLF([(0, 2), (2, 0), (5, 1), (8, -2)])
    new_a_1, new_a_2 = match_plf(a, a)
    assert new_a_1 == a
    assert new_a_2 == a


def test_5():
    a = PLF([])
    b = PLF([(0, 0)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == a


def test_6():
    a = PLF([])
    new_a_1, new_a_2 = match_plf(a, a)
    assert new_a_1 == a
    assert new_a_2 == a


def test_7():
    a = PLF([(3, -1)])
    b = PLF([(-2, 5)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([])
    assert new_b == PLF([])


def test_8():
    a = PLF([(-2, -1)])
    b = PLF([(-2, 5)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == b


def test_9():
    a = PLF([(-2, -1)])
    b = PLF([(-3, 5), (-1, 6)])
    new_a, new_b = match_plf(a, b)
    assert new_a == a
    assert new_b == PLF([(-2, 5.5)])


def test_10():
    a = PLF([(-1, 0), (1, 0)])
    b = PLF([(-2, 1), (0, 0), (2, 1)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(-1, 0), (0, 0), (1, 0)])
    assert new_b == PLF([(-1, 0.5), (0, 0), (1, 0.5)])


def test_11():
    a = PLF([(-1, 0), (0, 0), (0, 1), (1, 1)])
    b = PLF([(-0.5, 0), (1.5, 2)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(-0.5, 0), (0, 0), (0, 1), (1, 1)])
    assert new_b == PLF([(-0.5, 0), (0, 0.5), (0, 0.5), (1, 1.5)])


def test_12():
    a = PLF([(0, 0), (4, 2), (4, 0)])
    b = PLF([(0, 0), (4, 3)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 0), (4, 2), (4, 0)])
    assert new_b == PLF([(0, 0), (4, 3), (4, 3)])


def test_13():
    a = PLF([(0, 0)])
    b = PLF([(0, 0), (0, 1)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 0), (0, 0)])
    assert new_b == PLF([(0, 0), (0, 1)])


def test_14():
    a = PLF([(0, 0)])
    b = PLF([(0, 0), (0, 0)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 0), (0, 0)])
    assert new_b == PLF([(0, 0), (0, 0)])


def test_15():
    a = PLF([(0, 1), (0.5, 0), (1, 0), (1, 1)])
    b = PLF([(0, 0), (1, 0), (1, -1)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 1), (0.5, 0), (1, 0), (1, 1)])
    assert new_b == PLF([(0, 0), (0.5, 0), (1, 0), (1, -1)])


def test_16():
    a = PLF([(0, 1), (0.5, 0), (0.5, 0), (1, 1)])
    b = PLF([(0, 0), (1, 0)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 1), (0.5, 0), (0.5, 0), (1, 1)])
    assert new_b == PLF([(0, 0), (0.5, 0), (0.5, 0), (1, 0)])


def test_18():
    a = PLF([(0, 1), (0.5, 0), (0.5, 0), (1, 1)])
    b = PLF([(0, 0), (0.5, 0), (1, 0)])
    new_a, new_b = match_plf(a, b)
    assert new_a == PLF([(0, 1), (0.5, 0), (0.5, 0), (1, 1)])
    assert new_b == PLF([(0, 0), (0.5, 0), (0.5, 0), (1, 0)])
