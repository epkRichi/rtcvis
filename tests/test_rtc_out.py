import pytest
from rtcvis import *


@pytest.mark.parametrize(
    "upper_service_in,lower_events_in,expected_upper_service_out",
    [
        # (
        #     [(0, 0), (30, 30)],
        #     [
        #         (0, 0),
        #         (10, 0),
        #         (10, 1),
        #         (20, 1),
        #         (20, 2),
        #         (25, 2),
        #         (25, 3),
        #         (27.5, 3),
        #         (27.5, 4),
        #         (30, 4),
        #         (30, 5),
        #     ],
        #     [(0, 0), (6, 6), (10, 6), (15, 10), (30, 10)],
        # ),
        (
            [(0, 0), (13, 13), (15, 13)],
            [
                (0, 0),
                (8, 0),
                (8, 1),
                (11, 1),
                (11, 3),
                (12, 3),
                (12, 4),
                (13, 4),
                (13, 6),
                (15, 6),
                (15, 9),
            ],
            [(0, 0), (4, 4), (15, 4)],
        )
    ],
)
class TestRTCOut:
    def test_upper_service_out(
        self, upper_service_in, lower_events_in, expected_upper_service_out
    ):
        upper_service_in_plf = PLF(upper_service_in)
        lower_events_in_plf = PLF(lower_events_in)
        expected_upper_service_out_plf = PLF(expected_upper_service_out)
        result = upper_service_out(
            upper_service_in=upper_service_in_plf, lower_events_in=lower_events_in_plf
        )
        assert result == expected_upper_service_out_plf
