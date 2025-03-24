from typing import Any
import numpy as np


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return type(other) is Point and other.x == self.x and other.y == self.y

    @classmethod
    def create_intersection(cls, a: "Point", b: "Point", x: float) -> "Point":
        assert a.x != b.x
        left, right = (a, b) if a.x < b.x else (b, a)

        slope = (right.y - left.y) / (right.x - left.x)
        segment_length = x - left.x
        d_y = slope * segment_length
        return Point(x, left.y + d_y)


class PLF:
    def __init__(self, points: list[Point]) -> None:
        assert len(points) >= 2
        assert points[0].x == 0
        assert all(points[i].x <= points[i + 1].x for i in range(len(points) - 1))
        self.points = points

    def __repr__(self):
        return f"PLF([{', '.join([repr(point) for point in self.points])}])"

    def __eq__(self, other):
        if type(other) is not PLF or len(self.points) != len(other.points):
            return False

        for a, b in zip(self.points, other.points):
            if a != b:
                return False

        return True

    @classmethod
    def match(cls, a: "PLF", b: "PLF") -> tuple["PLF", "PLF"]:
        # if len(a.points) == 0 or len(b.points) == 0:
        #     return PLF([])

        # if len(a.points) == 1 and (
        #     b.points[0] > a.points[0].x or b.points[-1] < a.points[0].x
        # ):
        #     return PLF([])

        # if len(b.points) == 1 and (
        #     a.points[0] > b.points[0].x or a.points[-1] < b.points[0].x
        # ):
        #     return PLF([])

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
                new_b.append(Point.create_intersection(b.points[b_idx], new_b[-1], a.points[a_idx].x))
                a_idx += 1
            else:
                # Insert a new point for a
                new_a.append(Point.create_intersection(a.points[a_idx], new_a[-1], b.points[b_idx].x))
                new_b.append(b.points[b_idx])
                b_idx += 1

            stop_a = a_idx == len(a.points)
            stop_b = b_idx == len(b.points)
            if stop_a and stop_b:
                break

            if stop_a or stop_b:
                raise RuntimeError("Reached one function's end before the other")

        return PLF(new_a), PLF(new_b)

    def __add__(self, other: "PLF") -> "PLF":
        a, b = PLF.match(self, other)
        new_points = [Point(p1.x, p1.y + p2.y) for p1, p2 in zip(a.points, b.points)]
        return PLF(new_points)

    def __sub__(self, other: "PLF") -> "PLF":
        a, b = PLF.match(self, other)
        new_points = [Point(p1.x, p1.y - p2.y) for p1, p2 in zip(a.points, b.points)]
        return PLF(new_points)

    def transformed(self, mirror: bool, offset: float) -> "PLF":
        """Creates a new PLF that is offset on the x-Axis and optionally mirrored on the y-Axis.
        Note that the function will first be mirrored and then offset. The function will also be
        truncated so that it doesn't contain any points at x<0.

        Args:
            mirror (bool): Whether the function should first be mirrored on the y-Axis.
            offset (float): Amount which will be added to each point's x-coordinate.

        Returns:
            PLF: The transformed function.
        """
        new_points: list[Point] = []
        factor = -1 if mirror else 1
        # iterate over the points in the order in which they'll be in the transformed function
        points = iter(self.points) if mirror else reversed(self.points)
        for point in points:
            new_x = factor * point.x + offset
            new_points.insert(0, Point(new_x, point.y))
            if new_x < 0:
                assert (
                    len(new_points) > 1
                )  # FIXME It should also be allowed to have a function that is defined by a single point
                # new_x is smaller than 0 -> replace the point with the intersection at the y-axis
                new_points[0] = Point.create_intersection(new_points[0], new_points[1], 0)
                # we've reached x=0, stop here
                break

        return PLF(new_points)
