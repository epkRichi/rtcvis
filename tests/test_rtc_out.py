import pytest
from rtcvis import *


@pytest.mark.parametrize(
    "upper_service_in,lower_service_in,upper_events_in,lower_events_in,expected_upper_service_out,expected_lower_service_out,expected_upper_events_out,expected_lower_events_out",  # noqa: E501
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
            PLF([(0, 0), (13, 13), (15, 13)]),
            PLF([(0, 0), (2, 0), (15, 13)]),
            PLF(
                [
                    (0, 0),
                    (0, 3),
                    (1, 3),
                    (1, 5),
                    (2, 5),
                    (2, 6),
                    (3, 6),
                    (3, 8),
                    (6, 8),
                    (6, 9),
                    (15, 9),
                ]
            ),
            PLF(
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
                ]
            ),
            PLF([(0, 0), (4, 4), (15, 4)]),
            PLF([(0, 0), (11, 0), (15, 4)]),
            PLF(
                [
                    # (0, 0),
                    (0, 1),
                    (1, 1),
                    (1, 2),
                    (2, 2),
                    (2, 3),
                    (3, 3),
                    (3, 4),
                    (4, 4),
                    (4, 5),
                    (5, 5),
                    (5, 6),
                    (6, 6),
                    (6, 7),
                    (7, 7),
                    (7, 8),
                    (8, 8),
                    (8, 9),
                    (13, 9),
                    (13, 10),
                    (14, 10),
                    (14, 11),
                    (15, 11),
                    (15, 12),
                ]
            ),
            PLF(
                [
                    # (0, 0),
                    (9, 0),
                    (9, 1),
                    (10, 1),
                    (10, 2),
                    (11, 2),
                    (11, 3),
                    (12, 3),
                    (12, 4),
                    (13, 4),
                    (13, 5),
                    (14, 5),
                    (14, 6),
                    (15, 6),
                    (15, 7),
                ]
            ),
        )
    ],
)
class TestRTCOut:
    def test_upper_service_out(
        self,
        upper_service_in,
        lower_service_in,
        upper_events_in,
        lower_events_in,
        expected_upper_service_out,
        expected_lower_service_out,
        expected_upper_events_out,
        expected_lower_events_out,
    ):
        result = upper_service_out(
            upper_service_in=upper_service_in, lower_events_in=lower_events_in
        )
        assert result == expected_upper_service_out

    def test_lower_service_out(
        self,
        upper_service_in,
        lower_service_in,
        upper_events_in,
        lower_events_in,
        expected_upper_service_out,
        expected_lower_service_out,
        expected_upper_events_out,
        expected_lower_events_out,
    ):
        result = lower_service_out(
            lower_service_in=lower_service_in, upper_events_in=upper_events_in
        )
        assert result == expected_lower_service_out

    def test_upper_events_out(
        self,
        upper_service_in,
        lower_service_in,
        upper_events_in,
        lower_events_in,
        expected_upper_service_out,
        expected_lower_service_out,
        expected_upper_events_out,
        expected_lower_events_out,
    ):
        result = upper_events_out(
            upper_events_in=upper_events_in,
            lower_service_in=lower_service_in,
            upper_service_in=upper_service_in,
        )
        assert result == expected_upper_events_out

    def test_lower_events_out(
        self,
        upper_service_in,
        lower_service_in,
        upper_events_in,
        lower_events_in,
        expected_upper_service_out,
        expected_lower_service_out,
        expected_upper_events_out,
        expected_lower_events_out,
    ):
        result = lower_events_out(
            lower_events_in=lower_events_in,
            lower_service_in=lower_service_in,
            upper_service_in=upper_service_in,
        )
        assert result == expected_lower_events_out
