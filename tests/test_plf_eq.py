from rtcvis.plf import Point, PLF

def test_point_eq():
    a = Point(0, 0)
    b = Point(0.0, 0.0)
    c = Point(0, 1)
    assert a == a
    assert a == b
    assert a != c

def test_plf_eq():
    a = PLF([Point(0, 0), Point(2, 1), Point(5, 3)])
    b = PLF([Point(0, 0), Point(2, 2), Point(5, 3)])
    assert a == a
    assert b == b
    assert a != b
