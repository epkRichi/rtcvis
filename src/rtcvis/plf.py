from typing import Any
import numpy as np


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __eq__(self, other):
        return type(other) is Point and other.x == self.x and other.y == self.y


class PLF:
    def __init__(self, points: list[Point]) -> None:
        assert len(points) >= 2
        assert points[0].x == 0
        assert all(points[i].x <= points[i+1].x for i in range(len(points) - 1))
        self.points = points

    def __repr__(self):
        return f"[{', '.join([repr(point) for point in self.points])}]"
    
    def __eq__(self, other):
        if type(other) is not PLF or len(self.points) != len(other.points):
            return False
        
        for a, b in zip(self.points, other.points):
            if a != b:
                return False
            
        return True
            
    @classmethod
    def match(cls, a: "PLF", b: "PLF") -> tuple["PLF", "PLF"]:
        new_a = [a.points[0]]
        new_b = [b.points[0]]
        a_idx = 1
        b_idx = 1

        while True:
            a_x = a.points[a_idx].x
            b_x = b.points[b_idx].x

            if a_x == b_x:
                new_a.append(a.points[a_idx])
                new_b.append(b.points[b_idx])
                a_idx += 1
                b_idx += 1
            elif a_x < b_x:
                slope = (b.points[b_idx].y - new_b[-1].y) / (b.points[b_idx].x - new_b[-1].x)
                segment_length = a.points[a_idx].x - new_b[-1].x
                d_y = slope * segment_length
                new_a.append(a.points[a_idx])
                new_b.append(Point(a.points[a_idx].x, new_b[-1].y + d_y))
                a_idx += 1
            else:
                slope = (a.points[a_idx].y - new_a[-1].y) / (a.points[a_idx].x - new_a[-1].x)
                segment_length = b.points[b_idx].x - new_a[-1].x
                d_y = slope * segment_length
                new_a.append(Point(b.points[b_idx].x, new_a[-1].y + d_y))
                new_b.append(b.points[b_idx])
                b_idx += 1

            stop_a = (a_idx == len(a.points))
            stop_b = (b_idx == len(b.points))
            if stop_a and stop_b:
                break
            
            if stop_a or stop_b:
                raise RuntimeError("Reached one function's end before the other")

        return PLF(new_a), PLF(new_b)
