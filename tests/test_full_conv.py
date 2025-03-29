from rtcvis import *
from rtcvis.conv import get_critical_points

# fmt: off
def test_critical_points_1():
    assert get_critical_points(PLF([]), PLF([]), False) == []
    assert get_critical_points(PLF([Point(0, 0)]), PLF([]), False) == []
    assert get_critical_points(PLF([]), PLF([Point(0, 0)]), False) == []
    assert get_critical_points(PLF([Point(0, 1)]), PLF([Point(0, 5)]), False) == [0]
    assert get_critical_points(PLF([Point(-1, 1)]), PLF([Point(0, 5)]), False) == [1]
    assert get_critical_points(PLF([Point(1, 1)]), PLF([Point(0, 5)]), False) == [-1]
    assert get_critical_points(PLF([Point(1, 1)]), PLF([Point(0, 5), Point(1, 5)]), False) == [-1, 0]
    assert get_critical_points(PLF([Point(1, 1)]), PLF([Point(0, 5), Point(1, 5)]), False) == [-1, 0]
    assert get_critical_points(PLF([Point(0, 5), Point(1, 5)]), PLF([Point(1, 1)]), False) == [0, 1]
    assert get_critical_points(PLF([Point(0, 5), Point(1, 5)]), PLF([Point(0.5, 1), Point(1.5, 3)]), False) == [-0.5, 0.5, 1.5]


def test_critical_points_2():
    assert get_critical_points(PLF([]), PLF([]), True) == []
    assert get_critical_points(PLF([Point(0, 0)]), PLF([]), True) == []
    assert get_critical_points(PLF([]), PLF([Point(0, 0)]), True) == []
    assert get_critical_points(PLF([Point(0, 1)]), PLF([Point(0, 5)]), True) == [0]
    assert get_critical_points(PLF([Point(-1, 1)]), PLF([Point(0, 5)]), True) == [1]
    assert get_critical_points(PLF([Point(1, 1)]), PLF([Point(0, 5)]), True) == []
    assert get_critical_points(PLF([Point(1, 1)]), PLF([Point(0, 5), Point(1, 5)]), True) == [0]
    assert get_critical_points(PLF([Point(1, 1)]), PLF([Point(0, 5), Point(1, 5)]), True) == [0]
    assert get_critical_points(PLF([Point(0, 5), Point(1, 5)]), PLF([Point(1, 1)]), True) == [0, 1]
    assert get_critical_points(PLF([Point(0, 5), Point(1, 5)]), PLF([Point(0.5, 1), Point(1.5, 3)]), True) == [0, 0.5, 1.5]

def test_min_plus_conv_1():
    conv_type = ConvType.MIN_PLUS_CONV
    a = PLF([Point(0, 2), Point(5, 4.5)])
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    result = get_full_plus_conv(a, b, conv_type)
    assert result.x_start == 0
    assert result.x_end == b.x_end + a.x_end
    assert result(0) == 2
    assert result(0.5) == 2
    assert result(1) == 2
    assert result(1.5) == 2.25
    assert result(2) == 2.5
    assert result(2.5) == 2.75
    assert result(3) == 3


def test_min_plus_conv_2():
    conv_type = ConvType.MIN_PLUS_CONV
    # convex PLFs that start at (0,0) -> reordering of segments in the order of least slope
    a = PLF([Point(0, 0), Point(2.5, 1), Point(6, 5.5)])
    b = PLF([Point(0, 0), Point(4, 1), Point(6.5, 5.5)])
    result = get_full_plus_conv(a, b, conv_type)
    assert result.x_start == 0
    assert result.x_end == b.x_end + a.x_end
    # segment 1 (b)
    assert result(0) == 0
    assert result(1) == 0.25
    assert result(2) == 0.5
    assert result(4) == 1
    # segment 2 (a)
    assert result(5) == 1.4
    assert result(6) == 1.8
    assert result(6.5) == 2
    # segment 3 (b)
    assert result(7.5) == 2 + 1 * (
        9 / 7
    )  # why did I choose such ugly numbers?
    assert result(8.5) == 2 + 2 * (9 / 7)
    assert result(10) == 2 + 3.5 * (9 / 7)
    # Segment 4 (a)
    assert result(11) == 2 + 3.5 * (9 / 7) + 1 * (9 / 5)
    assert result(12) == 2 + 3.5 * (9 / 7) + 2 * (9 / 5)
    assert result(12.5) == 2 + 3.5 * (9 / 7) + 2.5 * (9 / 5)


def test_max_plus_conv_1():
    conv_type = ConvType.MAX_PLUS_CONV
    a = PLF([Point(0, 2), Point(5, 4.5)])
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    result = get_full_plus_conv(a, b, conv_type)
    assert result.x_start == 0
    assert result.x_end == b.x_end + a.x_end
    assert result(0) == 2
    assert result(0.5) == 2.25
    assert result(1) == 2.5
    assert result(1.5) == 2.75
    assert result(2) == 3
    assert result(2.5) == 3.25
    assert result(3) == 3.5


def test_min_plus_deconv_1():
    conv_type = ConvType.MIN_PLUS_DECONV
    a = PLF([Point(0, 2), Point(12, 5)])  # slope 0.25
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    result = get_full_plus_conv(a, b, conv_type)
    assert result.x_start == 0
    assert result.x_end == a.x_end
    assert result(0) == 2.25
    assert result(1) == 2.5
    assert result(2) == 2.75
    assert result(3) == 3


def test_max_plus_deconv_1():
    conv_type = ConvType.MAX_PLUS_DECONV
    a = PLF([Point(0, 2), Point(12, 5)])  # slope 0.25
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    result = get_full_plus_conv(a, b, conv_type)
    assert result.x_start == 0
    assert result.x_end == a.x_end
    assert result(0) == 1
    assert result(1) == 1.25
    assert result(2) == 1.5
    assert result(3) == 1.75
