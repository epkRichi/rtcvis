import pytest
from rtcvis import PLF


def test_1():
    # check that simplified doesn't modify PLFs with less than 3 points
    a = PLF([])
    assert a == a.simplified()
    a = PLF([(0, 5)])
    assert a == a.simplified()
    a = PLF([(0, 3), (2, 5)])
    assert a == a.simplified()
    a = PLF([(0, 3), (0, 4)])
    assert a == a.simplified()
    # check that PLFs without redundant points also dont get modified
    a = PLF([(1, 1), (2, 2), (3, 1)])
    assert a == a.simplified()
    a = PLF([(1, 1), (2, 2), (2, 3)])
    assert a == a.simplified()
    a = PLF([(0, 1), (0, 0), (1, 0)])
    assert a == a.simplified()
    # now check whether the simplification actually works
    a = PLF([(0, 0), (1, 0), (2, 0)])
    b = PLF([(0, 0), (2, 0)])
    assert a.simplified() == b
    a = PLF([(0, 0), (1, 1), (2, 2)])
    b = PLF([(0, 0), (2, 2)])
    assert a.simplified() == b
    a = PLF([(0, 0), (1, 1), (2, 2), (3, 3)])
    b = PLF([(0, 0), (3, 3)])
    assert a.simplified() == b
    a = PLF([(0, 0), (1, 1), (2, 2), (2, 3), (3, 3), (4, 3), (4, 0), (5, 1), (6, 2)])
    b = PLF([(0, 0), (2, 2), (2, 3), (4, 3), (4, 0), (6, 2)])
    assert a.simplified() == b


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            [
                (0, 2.0),
                (0, 2.0),
                (0.25, 2.25),
                (0.5, 2.0),
                (1, 1.5),
                (1, 1.5),
                (1.75, 1.5),
                (2, 1),
                (2, 1),
            ],
            [(0, 2), (0.25, 2.25), (1, 1.5), (1.75, 1.5), (2, 1)],
        )
    ],
)
def test_2(input, expected):
    input_plf = PLF(input)
    expected_plf = PLF(expected)
    result = input_plf.simplified()
    assert result == expected_plf
