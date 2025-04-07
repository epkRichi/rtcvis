import pytest
from rtcvis import *
from rtcvis.plf import plf_merge


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # Trivial cases
        ([], [], []),
        ([], [(1, 1)], [(1, 1)]),
        ([(1, 1)], [], [(1, 1)]),
        # b is defined before and after a
        (
            [(0, 0), (1, 0)],
            [(-1, 1), (2, 1)],
            [(-1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (2, 1)],
        ),
        # a has a redundant point at the end
        (
            [(0, 0), (1, 0), (1, 10)],
            [(-1, 1), (2, 1)],
            [(-1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (2, 1)],
        ),
        # a and b start and end at the same x
        (
            [(0, 0), (1, 0)],
            [(0, 0), (1, 1)],
            [(0, 0), (1, 0)],
        ),
    ],
)
def test_plf_merge(a, b, expected):
    a_plf = PLF(a)
    b_plf = PLF(b)
    result = plf_merge(a_plf, b_plf)
    expected_plf = PLF(expected)
    assert result == expected_plf
