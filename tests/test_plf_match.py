from rtcvis.plf import Point, PLF

def test_1():
    a = PLF([Point(0, 0), Point(2, 2)])
    b = PLF([Point(0, 0), Point(1, 0.5), Point(2, 2.5)])
    new_a, new_b = PLF.match(a, b)
    assert new_a == PLF([Point(0, 0), Point(1, 1), Point(2, 2)])
    assert new_b == b

def test_2():
    a = PLF([Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 1)])
    b = PLF([Point(0, 1), Point(2, 3)])
    new_a, new_b = PLF.match(a, b)
    assert new_a == a
    assert new_b == PLF([Point(0, 1), Point(1, 2), Point(1, 2), Point(2, 3)])
