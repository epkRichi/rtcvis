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
        if len(points) > 1:
            # the points have to be given with ascending x coordinates
            assert all(points[i].x <= points[i + 1].x for i in range(len(points) - 1))
        if len(points) > 2:
            # there can be at most 2 points at the same x coordinate
            assert all(
                (points[i].x != points[i + 1].x) or (points[i + 1].x != points[i + 2].x)
                for i in range(len(points) - 2)
            )

        if len(points) == 0:
            self.x_start = 0
            self.x_end = 0
        else:
            self.x_start = points[0].x
            self.x_end = points[-1].x

        self.points = points

    def __repr__(self):
        return f"PLF([{', '.join([repr(point) for point in self.points])}])"

    def __eq__(self, other):
        if type(other) is not PLF or len(self.points) != len(other.points):
            return False

        return all(a == b for a, b in zip(self.points, other.points))

    def trunc_start(self, x_start: float) -> "PLF":
        if self.x_start >= x_start:
            return self

        for idx, point in enumerate(self.points):
            if point.x >= x_start:
                points = []
                if point.x > x_start:
                    points = [
                        Point.create_intersection(
                            self.points[idx - 1], self.points[idx], x_start
                        )
                    ]
                points += self.points[idx:]
                return PLF(points)
        return PLF([])

    def trunc_end(self, x_end: float) -> "PLF":
        if self.x_end <= x_end:
            return self

        for idx, point in reversed(list(enumerate(self.points))):
            if point.x <= x_end:
                points = []
                if point.x < x_end:
                    points = [
                        Point.create_intersection(
                            self.points[idx + 1], self.points[idx], x_end
                        )
                    ]
                points = self.points[: idx + 1] + points
                return PLF(points)
        return PLF([])

    @classmethod
    def match(cls, a: "PLF", b: "PLF") -> tuple["PLF", "PLF"]:
        if len(a.points) == 0 or len(b.points) == 0:
            return PLF([]), PLF([])

        # Truncate the functions so they start/end at the same x coordinates
        a = a.trunc_start(b.x_start).trunc_end(b.x_end)
        b = b.trunc_start(a.x_start).trunc_end(a.x_end)

        if len(a.points) <= 1:
            # If either function now has at most 1 point, the other function will
            # already have the same number of points and they'll be at the same
            # x coordinates, so we can stop here
            return a, b

        # both functions have at least 2 points
        # Note that even if one has exactly 2 points, the other one might have more than that
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
                new_b.append(
                    Point.create_intersection(
                        b.points[b_idx], new_b[-1], a.points[a_idx].x
                    )
                )
                a_idx += 1
            else:
                # Insert a new point for a
                new_a.append(
                    Point.create_intersection(
                        a.points[a_idx], new_a[-1], b.points[b_idx].x
                    )
                )
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
        Note that the function will first be mirrored and then offset.

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

        return PLF(new_points)
