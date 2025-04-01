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
