from rtcvis.point import Point, line_intersection


def test_1():
    # normal line intersections
    i = line_intersection(Point(0, 0), Point(1, 1), Point(0, 1), Point(1, 0))
    assert i == Point(0.5, 0.5)
    i = line_intersection(Point(0, 0), Point(1, 1), Point(1, 1), Point(2, 0))
    assert i == Point(1, 1)
    i = line_intersection(Point(-1, -1), Point(1, 0), Point(2, 4), Point(4, -2))
    assert i == Point(3, 1)
    # first and second point swapped
    i = line_intersection(Point(1, 0), Point(-1, -1), Point(2, 4), Point(4, -2))
    assert i == Point(3, 1)
    # parallel lines, both identical and different
    i = line_intersection(Point(0, 0), Point(1, 0), Point(5, 6), Point(3, 6))
    assert i is None
    i = line_intersection(Point(0, 0), Point(1, 0), Point(0, 0), Point(1, 0))
    assert i is None
    i = line_intersection(Point(0, 0), Point(1, 0), Point(-1, 0), Point(3, 0))
    assert i is None
    # two vertical lines, both identical and different
    i = line_intersection(Point(0, 0), Point(0, -5), Point(0, 0), Point(0, -5))
    assert i is None
    i = line_intersection(Point(0, 0), Point(0, -5), Point(0, -1), Point(0, 3))
    assert i is None
    i = line_intersection(Point(0, 0), Point(0, -5), Point(2, -1), Point(2, 3))
    assert i is None
    # one vertical line, one non-vertical line
    i = line_intersection(Point(0, 0), Point(0, -5), Point(-1, 0), Point(1, 1))
    assert i == Point(0, 0.5)
    i = line_intersection(Point(0, 0), Point(0, -5), Point(-1, 0), Point(1, 0))
    assert i == Point(0, 0)
