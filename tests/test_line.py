import pytest

from rtcvis.point import Point
from rtcvis.line import Line, line_intersection


def test_init():
    # Check that init works with both Points and Tuples
    Line((0, 0), (1, 0))
    Line((0, 0), Point(1, 0))
    Line(Point(0, 0), (1, 0))
    Line(Point(0, 0), Point(1, 0))
    # Check the properties of a "normal" line
    line = Line((0, 0), (1, 1))
    assert line.a == Point(0, 0)
    assert line.b == Point(1, 1)
    assert line.slope == 1
    assert not line.is_vertical
    # Check the properties of a line with slope 0 and swapped points
    line = Line((1, 0), (0, 0))
    assert line.a == Point(0, 0)
    assert line.b == Point(1, 0)
    assert line.slope == 0
    assert not line.is_vertical
    # Check that Vertical lines can be created
    line = Line((0, 0), (0, 1))
    assert line.a == Point(0, 0)
    assert line.b == Point(0, 1)
    assert line.slope is None
    assert line.is_vertical
    # Check that lines can't be created from identical Points
    with pytest.raises(AssertionError):
        Line((3, 3), (3, 3))


def test_line_intersection():
    # normal line intersections
    i = line_intersection(Line((0, 0), (1, 1)), Line((0, 1), (1, 0)))
    assert i == (0.5, 0.5)
    i = line_intersection(Line((0, 0), (1, 1)), Line((1, 1), (2, 0)))
    assert i == (1, 1)
    i = line_intersection(Line((-1, -1), (1, 0)), Line((2, 4), (4, -2)))
    assert i == (3, 1)
    # first and second point swapped
    i = line_intersection(Line((1, 0), (-1, -1)), Line((2, 4), (4, -2)))
    assert i == (3, 1)
    # parallel lines, both identical and different
    i = line_intersection(Line((0, 0), (1, 0)), Line((5, 6), (3, 6)))
    assert i is None
    i = line_intersection(Line((0, 0), (1, 0)), Line((0, 0), (1, 0)))
    assert i is None
    i = line_intersection(Line((0, 0), (1, 0)), Line((-1, 0), (3, 0)))
    assert i is None
    # two vertical lines, both identical and different
    i = line_intersection(Line((0, 0), (0, -5)), Line((0, 0), (0, -5)))
    assert i is None
    i = line_intersection(Line((0, 0), (0, -5)), Line((0, -1), (0, 3)))
    assert i is None
    i = line_intersection(Line((0, 0), (0, -5)), Line((2, -1), (2, 3)))
    assert i is None
    # one vertical line, one non-vertical line
    i = line_intersection(Line((0, 0), (0, -5)), Line((-1, 0), (1, 1)))
    assert i == (0, 0.5)
    i = line_intersection(Line((0, 0), (0, -5)), Line((-1, 0), (1, 0)))
    assert i == (0, 0)
