from typing import Optional


class Point:
    def __init__(self, x: float, y: float) -> None:
        """A 2D point with coordinates x and y.

        Objects of this class should not be mutated.

        Args:
            x (float): x coordinate
            y (float): y coordinate
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return type(other) is Point and other.x == self.x and other.y == self.y


def point_on_line(a: Point, b: Point, x: float) -> Point:
    """Creates a new point on the line from a through b.

    Note that a and b are not allowed to have the same x coordinates.

    Args:
        a (Point): First point
        b (Point): Second point
        x (float): x coordinate of the new point

    Returns:
        Point: The point on the straight line at the given x.
    """
    assert a.x != b.x
    left, right = (a, b) if a.x < b.x else (b, a)

    slope = (right.y - left.y) / (right.x - left.x)
    segment_length = x - left.x
    d_y = slope * segment_length
    return Point(x, left.y + d_y)


def line_intersection(a1: Point, a2: Point, b1: Point, b2: Point) -> Optional[Point]:
    """Computes the intersection of two lines.

    The lines are defined by two points each.

    Args:
        a1 (Point): First point of line a.
        a2 (Point): Second point of line a.
        b1 (Point): First point of line b.
        b2 (Point): Second point of line b.

    Returns:
        Optional[Point]: The intersection of lines a and b if there is exactly one,
            else None.
    """
    a_vert = a2.x == a1.x
    if not a_vert:
        m_a = (a2.y - a1.y) / (a2.x - a1.x)

    b_vert = b2.x == b1.x
    if not b_vert:
        m_b = (b2.y - b1.y) / (b2.x - b1.x)

    if a_vert and b_vert:
        return None

    if a_vert:
        return Point(a1.x, m_b * (a1.x - b1.x) + b1.y)

    if b_vert:
        return Point(b1.x, m_a * (b1.x - a1.x) + a1.y)

    if m_a == m_b:
        return None

    x = (b1.y - a1.y + m_a * a1.x - m_b * b1.x) / (m_a - m_b)
    y = m_a * (x - a1.x) + a1.y

    return Point(x, y)
