import pytest

from rtcvis.plf import PLF, plf_max


@pytest.mark.parametrize(
    "a,b,expected",
    [
        ([], [(0, 1), (1, 3)], []),
        ([(1, 1)], [(1, 1.2)], [(1, 1.2)]),
        ([(1, 1), (2, 1)], [(1, 1.2), (2, 1.2)], [(1, 1.2), (2, 1.2)]),
        (
            [(0, 0), (1, 0), (2, 1)],
            [(0, 0), (1, 1), (2, 0)],
            [(0, 0), (1, 1), (1.5, 0.5), (2, 1)],
        ),
        (
            [(0, 0), (1, 1), (2, 0)],
            [(0, 1), (1, 0), (2, 1)],
            [(0, 1), (0.5, 0.5), (1, 1), (1.5, 0.5), (2, 1)],
        ),
        (
            [(0, -1), (1, 1), (2, 1), (3, 0), (4, 1), (5, 0), (6, 1)],
            [(0, 0), (6, 0)],
            [(0, 0), (0.5, 0), (1, 1), (2, 1), (3, 0), (4, 1), (5, 0), (6, 1)],
        ),
        (
            [(0, 1), (2, -1), (3, 0), (4, -1), (5, 0), (6, -1), (7, 0)],
            [(0, 0), (7, 0)],
            [(0, 1), (1, 0), (7, 0)],
        ),
    ],
)
def test_plf_max_normal(a, b, expected):
    plf_a = PLF(a)
    plf_b = PLF(b)
    plf_expected = PLF(expected)
    result = plf_max(plf_a, plf_b)
    assert result == plf_expected


@pytest.mark.parametrize("a", [[], [(0, 0)], [(0, 0), (1, 1), (2, 1), (3, 0)]])
def test_plf_max_identical(a):
    plf_a = PLF(a)
    result = plf_max(plf_a, plf_a)
    assert result == plf_a
