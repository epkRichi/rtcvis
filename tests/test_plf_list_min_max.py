import pytest
from rtcvis import *
from rtcvis.plf import plf_list_min_max


@pytest.mark.parametrize(
    "plfs,expected",
    [
        (
            [
                [(0, 0), (1, 2), (2, 2)],
                [(0, 0.5), (1.5, 0.5), (2, 2.5), (2.5, 2.5)],
            ],
            [(0, 0), (0.25, 0.5), (1.5, 0.5), (1.875, 2), (2, 2), (2, 2.5), (2.5, 2.5)],
        )
    ],
)
def test_plf_list_min(plfs, expected):
    plfs_plf = [PLF(plf) for plf in plfs]
    expected_plf = PLF(expected)
    result = plf_list_min_max(plfs_plf, compute_min=True)
    assert result == expected_plf
