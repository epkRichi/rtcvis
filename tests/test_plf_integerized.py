import pytest
from rtcvis import *


@pytest.mark.parametrize(
    "plf,expected",
    [
        # empty PLF
        (
            PLF([]),
            PLF([]),
        ),
        # PLFs with only 1 Point
        (
            PLF([(0.3, 1.1)]),
            PLF([(0.3, 1)]),
        ),
        (
            PLF([(0, 0)]),
            PLF([(0, 0)]),
        ),
        # two point PLFs that get floored to 1 value
        (
            PLF([(0, 0), (0.9, 0.9)]),
            PLF([(0, 0), (0.9, 0)]),
        ),
        (
            PLF([(0.3, 0.5), (0.7, 0.1)]),
            PLF([(0.3, 0), (0.7, 0)]),
        ),
        (
            PLF([(0, 0), (1, 0)]),
            PLF([(0, 0), (1, 0)]),
        ),
        (PLF([(0, 1), (1, 0)]), PLF([(0, 0), (1, 0)])),
        # PLFs with two points that get floored into mulitple stairs
        (
            PLF([(0, 0), (2, 2)]),
            PLF([(0, 0), (1, 0), (1, 1), (2, 1)]),
        ),
        (
            PLF([(0, 0), (1, 2)]),
            PLF([(0, 0), (0.5, 0), (0.5, 1), (1, 1)]),
        ),
        # PLFs with multiple points
        (
            PLF(
                [
                    (0, 0.5),
                    (1, 1.5),
                    (2, 1.1),
                    (3, 2.1),
                    (4, 2),
                    (5, 2.9),
                    (6, 2.9),
                    (7, 3.1),
                ]
            ),
            PLF(
                [
                    (0, 0),
                    (0.5, 0),
                    (0.5, 1),
                    (2.9, 1),
                    (2.9, 2),
                    (6.5, 2),
                    (6.5, 3),
                    (7, 3),
                ]
            ),
        ),
        # PLF with discontinuity at start and end
        (
            PLF([(0, 0.3), (0, 2.1), (1, 2.5), (2, 3.5), (2, 4.5)]),
            PLF([(0, 2), (1.5, 2), (1.5, 3), (2, 3)]),
        ),
    ],
)
def test_plf_floored(plf: PLF, expected: PLF):
    result = plf.floored()
    assert result == expected


@pytest.mark.parametrize(
    "plf,expected",
    [
        # empty PLF
        (
            PLF([]),
            PLF([]),
        ),
        # PLFs with only 1 Point
        (
            PLF([(0.3, 1.1)]),
            PLF([(0.3, 2)]),
        ),
        (
            PLF([(0, 0)]),
            PLF([(0, 0)]),
        ),
        # two point PLFs that get floored to 1 value
        (
            PLF([(0, 0), (0.9, 0.9)]),
            PLF([(0, 1), (0.9, 1)]),
        ),
        (
            PLF([(0.3, 0.5), (0.7, 0.1)]),
            PLF([(0.3, 1), (0.7, 1)]),
        ),
        (
            PLF([(0, 0), (1, 0)]),
            PLF([(0, 0), (1, 0)]),
        ),
        (PLF([(0, 1), (1, 0)]), PLF([(0, 1), (1, 1)])),
        # PLFs with two points that get floored into mulitple stairs
        (
            PLF([(0, 0), (2, 2)]),
            PLF([(0, 1), (1, 1), (1, 2), (2, 2)]),
        ),
        (
            PLF([(0, 0), (1, 2)]),
            PLF([(0, 1), (0.5, 1), (0.5, 2), (1, 2)]),
        ),
        # PLFs with multiple points
        (
            PLF(
                [
                    (0, 0.5),
                    (1, 1.5),
                    (2, 1.1),
                    (3, 2.1),
                    (4, 2),
                    (5, 2.9),
                    (6, 2.9),
                    (7, 3.1),
                ]
            ),
            PLF(
                [
                    (0, 1),
                    (0.5, 1),
                    (0.5, 2),
                    (2.9, 2),
                    (2.9, 3),
                    (6.5, 3),
                    (6.5, 4),
                    (7, 4),
                ]
            ),
        ),
        # PLF with discontinuity at start and end
        (
            PLF([(0, 0.3), (0, 2.1), (1, 2.5), (2, 3.5), (2, 4.5)]),
            PLF([(0, 3), (1.5, 3), (1.5, 4), (2, 4)]),
        ),
    ],
)
def test_plf_ceiled(plf: PLF, expected: PLF):
    result = plf.ceiled()
    assert result == expected
