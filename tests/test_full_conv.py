from rtcvis import *
from rtcvis.conv import get_critical_points


def test_critical_points_1():
    # cp will return the points for a being shifted to the right (confusing, ik)
    def cp(a, b):
        return get_critical_points(b, a, ConvType.MAX_PLUS_DECONV, None, None)

    assert cp(PLF([]), PLF([])) == []
    assert cp(PLF([(0, 0)]), PLF([])) == []
    assert cp(PLF([]), PLF([(0, 0)])) == []
    assert cp(PLF([(0, 1)]), PLF([(0, 5)])) == [0]
    assert cp(PLF([(-1, 1)]), PLF([(0, 5)])) == [1]
    assert cp(PLF([(1, 1)]), PLF([(0, 5)])) == [-1]
    assert cp(PLF([(1, 1)]), PLF([(0, 5), (1, 5)])) == [-1, 0]
    assert cp(PLF([(1, 1)]), PLF([(0, 5), (1, 5)])) == [-1, 0]
    assert cp(PLF([(0, 5), (1, 5)]), PLF([(1, 1)])) == [0, 1]
    assert cp(PLF([(0, 5), (1, 5)]), PLF([(0.5, 1), (1.5, 3)])) == [
        -0.5,
        0.5,
        1.5,
    ]


def test_critical_points_2():
    # cp will return the points for a being shifted to the right (confusing, ik)
    def cp(a, b):
        return get_critical_points(b, a, ConvType.MAX_PLUS_DECONV, 0, None)

    assert cp(PLF([]), PLF([])) == []
    assert cp(PLF([(0, 0)]), PLF([])) == []
    assert cp(PLF([]), PLF([(0, 0)])) == []
    assert cp(PLF([(0, 1)]), PLF([(0, 5)])) == [0]
    assert cp(PLF([(-1, 1)]), PLF([(0, 5)])) == [1]
    assert cp(PLF([(1, 1)]), PLF([(0, 5)])) == []
    assert cp(PLF([(1, 1)]), PLF([(0, 5), (1, 5)])) == [0]
    assert cp(PLF([(1, 1)]), PLF([(0, 5), (1, 5)])) == [0]
    assert cp(PLF([(0, 5), (1, 5)]), PLF([(1, 1)])) == [0, 1]
    assert cp(PLF([(0, 5), (1, 5)]), PLF([(0.5, 1), (1.5, 3)])) == [
        0,
        0.5,
        1.5,
    ]


def test_min_plus_conv_1():
    conv_type = ConvType.MIN_PLUS_CONV
    a = PLF([(0, 2), (5, 4.5)])
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    result = conv(a, b, conv_type)
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
    # convex PLFs that start at (0,0)
    # -> reordering of segments in the order of least slope
    a = PLF([(0, 0), (2.5, 1), (6, 5.5)])
    b = PLF([(0, 0), (4, 1), (6.5, 5.5)])
    result = conv(a, b, conv_type)
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
    assert result(7.5) == 2 + 1 * (9 / 7)  # why did I choose such ugly numbers?
    assert result(8.5) == 2 + 2 * (9 / 7)
    assert result(10) == 2 + 3.5 * (9 / 7)
    # Segment 4 (a)
    assert result(11) == 2 + 3.5 * (9 / 7) + 1 * (9 / 5)
    assert result(12) == 2 + 3.5 * (9 / 7) + 2 * (9 / 5)
    assert result(12.5) == 2 + 3.5 * (9 / 7) + 2.5 * (9 / 5)


def test_min_plus_conv_3():
    conv_type = ConvType.MIN_PLUS_CONV
    a = PLF([(0, 1.5), (0, 2), (1, 1), (2, 1)])
    b = PLF([(0, 0.5), (0.5, 1), (1, 0), (2, 0)])
    expected = PLF([(0, 2), (0.25, 2.25), (1, 1.5), (1.5, 1.5), (2, 1)])
    result = conv(
        a,
        b,
        conv_type,
    )
    simplified = result.simplified()
    assert simplified == expected


def test_max_plus_conv_1():
    conv_type = ConvType.MAX_PLUS_CONV
    a = PLF([(0, 2), (5, 4.5)])
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    result = conv(a, b, conv_type)
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
    a = PLF([(0, 2), (12, 5)])  # slope 0.25
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    result = conv(a, b, conv_type, 0)
    assert result.x_start == 0
    assert result.x_end == a.x_end
    assert result(0) == 2.25
    assert result(1) == 2.5
    assert result(2) == 2.75
    assert result(3) == 3


def test_max_plus_deconv_1():
    conv_type = ConvType.MAX_PLUS_DECONV
    a = PLF([(0, 2), (12, 5)])  # slope 0.25
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    result = conv(a, b, conv_type, 0)
    assert result.x_start == 0
    assert result.x_end == a.x_end
    assert result(0) == 1
    assert result(1) == 1.25
    assert result(2) == 1.5
    assert result(3) == 1.75


def test_max_plus_deconv_2():
    conv_type = ConvType.MAX_PLUS_DECONV
    a = PLF(
        [
            (0, 0),
            (8, 8),
            (8, 7),
            (11, 10),
            (11, 8),
            (12, 9),
            (12, 8),
            (13, 9),
            (13, 7),
            (15, 7),
            (15, 4),
        ]
    )
    b = PLF([(0, 0), (15, 0)])
    result = conv(a, b, conv_type, 0)
    simplified = result.simplified()
    expected = PLF([(0, 0), (4, 4), (15, 4)])
    assert simplified == expected
