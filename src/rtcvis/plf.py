from typing import Sequence
from rtcvis.point import Point
from rtcvis.line import Line


class PLF:
    def __init__(self, points: Sequence[Point | tuple[float, float]]) -> None:
        """A piecewise linear function defined by a list of points.

        The function must be defined at everywhere between the first and the last point.
        It is allowed to have discontinuities by specifying two points at the same x
        coordinate. The function may also have only 1 or 0 points.

        Args:
            points (Sequence[Point | tuple[float, float]]): The points which define the
                PLF. They must be in the correct order (x may not decrease). The list
                elements can either be Point instances or tuples of x and y coordinates.
        """
        self._points = _points = [
            p if isinstance(p, Point) else Point(*p) for p in points
        ]
        self._x = _x = [p.x for p in _points]
        self._y = _y = [p.y for p in _points]

        if len(_points) > 1:
            # the points have to be given with ascending x coordinates
            assert all(_x[i] <= _x[i + 1] for i in range(len(_points) - 1))
        if len(_points) > 2:
            # there can be at most 2 _points at the same x coordinate
            assert all(
                (_x[i] != _x[i + 1]) or (_x[i + 1] != _x[i + 2])
                for i in range(len(_points) - 2)
            )

        if len(_points) == 0:
            self._x_start = 0.0
            self._x_end = 0.0
            self._min = Point(0, 0)
            self._max = Point(0, 0)
        else:
            self._x_start = _x[0]
            self._x_end = _x[-1]
            self._min = Point(_x[_y.index(min(_y))], min(_y))
            self._max = Point(_x[_y.index(max(_y))], max(_y))

    @property
    def x_start(self):
        return self._x_start

    @property
    def x_end(self):
        return self._x_end

    @property
    def points(self):
        return self._points

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self) -> str:
        return f"PLF([{', '.join([repr(point) for point in self.points])}])"

    def __eq__(self, other) -> bool:
        if type(other) is not PLF or len(self.points) != len(other.points):
            return False

        return all(a == b for a, b in zip(self.points, other.points))

    def start_truncated(self, x_start: float) -> "PLF":
        """Creates a new PLF that is truncated at the start.

        The new PLF has the same function values at all x >= x_start, but it is not
        defined for any x < x_start.

        Args:
            x_start (float): The x coordinate at which to truncate the PLF.

        Returns:
            PLF: The truncated PLF.
        """
        if self.x_start >= x_start:
            return self

        for idx, point in enumerate(self.points):
            if point.x >= x_start:
                # This is the first point located after x_start
                points = []
                if point.x > x_start:
                    # create a new point at x_start if there isn't one already
                    new_point = Line(self.points[idx - 1], self.points[idx]).point_at_x(
                        x_start
                    )
                    assert new_point is not None
                    points = [new_point]
                # append all remaining points
                points += self.points[idx:]
                return PLF(points)
        return PLF([])

    def end_truncated(self, x_end: float) -> "PLF":
        """Creates a new PLF that is truncated at the end.

        The new PLF has the same function values at all x <= x_end, but it is not
        defined for any x > x_end.

        Args:
            x_end (float): The x coordinate at which to truncate the PLF.

        Returns:
            PLF: The truncated PLF.
        """
        if self.x_end <= x_end:
            return self

        for idx, point in reversed(list(enumerate(self.points))):
            if point.x <= x_end:
                # This is the first point located before x_start
                points = []
                if point.x < x_end:
                    # create a new point at x_end if there isn't one already
                    new_point = Line(self.points[idx + 1], self.points[idx]).point_at_x(
                        x_end
                    )
                    assert new_point is not None
                    points = [new_point]
                # prepend all remaining points
                points = list(self.points[: idx + 1]) + points
                return PLF(points)
        return PLF([])

    def __add__(self, other: "PLF") -> "PLF":
        """Adds the other function to self.

        The result will be returned and self will not be modified.

        Args:
            other (PLF): The other function to add to self.

        Returns:
            PLF: The sum of the two functions.
        """
        a, b = match_plf(self, other)
        new_points = [Point(p1.x, p1.y + p2.y) for p1, p2 in zip(a.points, b.points)]
        return PLF(new_points)

    def __sub__(self, other: "PLF") -> "PLF":
        """Subtracts the other function from self.

        The result will be returned and self will not be modified.

        Args:
            other (PLF): The other function to subtract from self.

        Returns:
            PLF: The sum of the two functions.
        """
        a, b = match_plf(self, other)
        new_points = [Point(p1.x, p1.y - p2.y) for p1, p2 in zip(a.points, b.points)]
        return PLF(new_points)

    def transformed(self, mirror: bool, offset: float) -> "PLF":
        """Used for creating shifted and mirrored PLFs.

        The new PLF is offset on the x-Axis and optionally mirrored on the y-Axis.
        Note that the function will first be mirrored and then offset, meaning that
        positive offset values will shift the function to the right.

        Args:
            mirror (bool): Whether the function should first be mirrored on the y-Axis.
            offset (float): Amount which will be added to each point's x-coordinate.

        Returns:
            PLF: The transformed function.
        """
        new_points: list[Point] = []
        factor = -1 if mirror else 1
        # iterate over the points in the order in which they'll be
        # in the transformed PLF
        points = iter(self.points) if mirror else reversed(self.points)
        for point in points:
            new_x = factor * point.x + offset
            new_points.insert(0, Point(new_x, point.y))

        return PLF(new_points)

    def get_value(self, x: float) -> float:
        """Computes and returns the value of this PLF at the given x.

        Args:
            x (float): x coordinate

        Returns:
            float: The result
        """
        assert len(self.points) > 0 and x >= self.x_start and x <= self.x_end
        for idx, p in enumerate(self.points):
            if p.x == x:
                return p.y
            elif p.x > x:
                p_at_x = Line(self.points[idx - 1], self.points[idx]).point_at_x(x)
                assert p_at_x is not None
                return p_at_x.y
        raise RuntimeError("Did not find points with corresponding x coordinates")

    def __call__(self, x: float) -> float:
        """Calls self.get_value(x)."""
        return self.get_value(x)


def match_plf(a: "PLF", b: "PLF") -> tuple["PLF", "PLF"]:
    """Matches two PLFs and returns the result.

    After matching the PLFs, they will have the same number of points and the points of
    those two functions will always be defined at the same x coordinates. The given
    PLFs will not be modified.

    Returns:
        tuple["PLF", "PLF"]: The matched functions.
    """
    if len(a.points) == 0 or len(b.points) == 0:
        return PLF([]), PLF([])

    # Truncate the functions so they start/end at the same x coordinates
    a = a.start_truncated(b.x_start).end_truncated(b.x_end)
    b = b.start_truncated(a.x_start).end_truncated(a.x_end)

    if len(a.points) <= 1:
        # If either function now has at most 1 point, the other function will
        # already have the same number of points and they'll be at the same
        # x coordinates, so we can stop here
        return a, b

    # both functions have at least 2 points. Note that even if one has exactly
    # 2 points, the other one might have more than that
    new_a = [a.points[0]]
    new_b = [b.points[0]]
    a_idx = 1
    b_idx = 1

    while True:
        a_x = a.points[a_idx].x
        b_x = b.points[b_idx].x

        if a_x == b_x:
            # The points are already at the same x coordinate
            new_a.append(a.points[a_idx])
            new_b.append(b.points[b_idx])
            a_idx += 1
            b_idx += 1
        elif a_x < b_x:
            # Insert a new point for b
            new_a.append(a.points[a_idx])
            new_b.append(Line(b.points[b_idx], new_b[-1]).point_at_x(a.points[a_idx].x))
            a_idx += 1
        else:
            # Insert a new point for a
            new_a.append(Line(a.points[a_idx], new_a[-1]).point_at_x(b.points[b_idx].x))
            new_b.append(b.points[b_idx])
            b_idx += 1

        # stop if we've just added the last point of both functions
        stop_a = a_idx == len(a.points)
        stop_b = b_idx == len(b.points)
        if stop_a and stop_b:
            break

        assert not (stop_a or stop_b), "Reached one function's end before the other"

    return PLF(new_a), PLF(new_b)


# def plf_max(a: PLF, b: PLF) -> PLF:
#     a, b = match_plf(a, b)
#     num_points = len(a.points)
#     new_points = []

#     for i in range(num_points - 1):
#         # append the point with the greater y
#         if a.y[i] >= b.y[i]:
#             new_points.append(a.points[i])
#         else:
#             new_points.append(b.points[i])

#         # check for an intersection in the next line segment
#         intersection = ((a.y[i] - b.y[i]) * (a.y[i+1] - b.y[i+1])) < 0
#         if intersection:
