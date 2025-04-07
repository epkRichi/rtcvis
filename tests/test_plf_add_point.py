import pytest
from rtcvis import *


@pytest.mark.parametrize(
    "plf,p,expected",
    [
        (PLF([]), Point(3, 5), PLF([])),
        (PLF([(0, 0)]), Point(3, 5), PLF([(3, 5)])),
        (PLF([(-1, 4)]), Point(3, 5), PLF([(2, 9)])),
        (PLF([(-1, 2), (1, -2)]), Point(3, 5), PLF([(2, 7), (4, 3)])),
    ],
)
def test_add_point(plf: PLF, p: Point, expected: PLF):
    result = plf.add_point(p)
    assert result == expected
