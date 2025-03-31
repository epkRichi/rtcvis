from rtcvis import *


def test_min_plus_conv_1():
    a = PLF([(0, 2), (5, 4.5)])
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    conv_type = ConvType.MIN_PLUS_CONV
    assert conv_at_x(a, b, 0, conv_type).result.y == 2
    assert conv_at_x(a, b, 0.5, conv_type).result.y == 2
    assert conv_at_x(a, b, 1, conv_type).result.y == 2
    assert conv_at_x(a, b, 1.5, conv_type).result.y == 2.25
    assert conv_at_x(a, b, 2, conv_type).result.y == 2.5
    assert conv_at_x(a, b, 2.5, conv_type).result.y == 2.75
    assert conv_at_x(a, b, 3, conv_type).result.y == 3


def test_min_plus_conv_2():
    # convex PLFs that start at (0,0) -> reordering of segments in the order of least slope
    a = PLF([(0, 0), (2.5, 1), (6, 5.5)])
    b = PLF([(0, 0), (4, 1), (6.5, 5.5)])
    conv_type = ConvType.MIN_PLUS_CONV
    # segment 1 (b)
    assert conv_at_x(a, b, 0, conv_type).result.y == 0
    assert conv_at_x(a, b, 1, conv_type).result.y == 0.25
    assert conv_at_x(a, b, 2, conv_type).result.y == 0.5
    assert conv_at_x(a, b, 4, conv_type).result.y == 1
    # segment 2 (a)
    assert conv_at_x(a, b, 5, conv_type).result.y == 1.4
    assert conv_at_x(a, b, 6, conv_type).result.y == 1.8
    assert conv_at_x(a, b, 6.5, conv_type).result.y == 2
    # segment 3 (b)
    assert conv_at_x(a, b, 7.5, conv_type).result.y == 2 + 1 * (
        9 / 7
    )  # why did I choose such ugly numbers?
    assert conv_at_x(a, b, 8.5, conv_type).result.y == 2 + 2 * (9 / 7)
    assert conv_at_x(a, b, 10, conv_type).result.y == 2 + 3.5 * (9 / 7)
    # Segment 4 (a)
    assert conv_at_x(a, b, 11, conv_type).result.y == 2 + 3.5 * (9 / 7) + 1 * (9 / 5)
    assert conv_at_x(a, b, 12, conv_type).result.y == 2 + 3.5 * (9 / 7) + 2 * (9 / 5)
    assert conv_at_x(a, b, 12.5, conv_type).result.y == 2 + 3.5 * (9 / 7) + 2.5 * (
        9 / 5
    )


def test_max_plus_conv_1():
    a = PLF([(0, 2), (5, 4.5)])
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    conv_type = ConvType.MAX_PLUS_CONV
    assert conv_at_x(a, b, 0, conv_type).result.y == 2
    assert conv_at_x(a, b, 0.5, conv_type).result.y == 2.25
    assert conv_at_x(a, b, 1, conv_type).result.y == 2.5
    assert conv_at_x(a, b, 1.5, conv_type).result.y == 2.75
    assert conv_at_x(a, b, 2, conv_type).result.y == 3
    assert conv_at_x(a, b, 2.5, conv_type).result.y == 3.25
    assert conv_at_x(a, b, 3, conv_type).result.y == 3.5


def test_min_plus_deconv_1():
    a = PLF([(0, 2), (12, 5)])  # slope 0.25
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    conv_type = ConvType.MIN_PLUS_DECONV
    assert conv_at_x(a, b, 0, conv_type).result.y == 2.25
    assert conv_at_x(a, b, 1, conv_type).result.y == 2.5
    assert conv_at_x(a, b, 2, conv_type).result.y == 2.75
    assert conv_at_x(a, b, 3, conv_type).result.y == 3


def test_max_plus_deconv_1():
    a = PLF([(0, 2), (12, 5)])  # slope 0.25
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    conv_type = ConvType.MAX_PLUS_DECONV
    assert conv_at_x(a, b, 0, conv_type).result.y == 1
    assert conv_at_x(a, b, 1, conv_type).result.y == 1.25
    assert conv_at_x(a, b, 2, conv_type).result.y == 1.5
    assert conv_at_x(a, b, 3, conv_type).result.y == 1.75
