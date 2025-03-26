from rtcvis import *


def test_min_plus_conv_1():
    a = PLF([Point(0, 2), Point(5, 4.5)])
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    assert min_plus_conv(a, b, 0)[1] == 2
    assert min_plus_conv(a, b, 0.5)[1] == 2
    assert min_plus_conv(a, b, 1)[1] == 2
    assert min_plus_conv(a, b, 1.5)[1] == 2.25
    assert min_plus_conv(a, b, 2)[1] == 2.5
    assert min_plus_conv(a, b, 2.5)[1] == 2.75
    assert min_plus_conv(a, b, 3)[1] == 3


def test_min_plus_conv_2():
    # convex PLFs that start at (0,0) -> reordering of segments in the order of least slope
    a = PLF([Point(0, 0), Point(2.5, 1), Point(6, 5.5)])
    b = PLF([Point(0, 0), Point(4, 1), Point(6.5, 5.5)])
    # segment 1 (b)
    assert min_plus_conv(a, b, 0)[1] == 0
    assert min_plus_conv(a, b, 1)[1] == 0.25
    assert min_plus_conv(a, b, 2)[1] == 0.5
    assert min_plus_conv(a, b, 4)[1] == 1
    # segment 2 (a)
    assert min_plus_conv(a, b, 5)[1] == 1.4
    assert min_plus_conv(a, b, 6)[1] == 1.8
    assert min_plus_conv(a, b, 6.5)[1] == 2
    # segment 3 (b)
    assert min_plus_conv(a, b, 7.5)[1] == 2 + 1 * (
        9 / 7
    )  # why did I choose such ugly numbers?
    assert min_plus_conv(a, b, 8.5)[1] == 2 + 2 * (9 / 7)
    assert min_plus_conv(a, b, 10)[1] == 2 + 3.5 * (9 / 7)
    # Segment 4 (a)
    assert min_plus_conv(a, b, 11)[1] == 2 + 3.5 * (9 / 7) + 1 * (9 / 5)
    assert min_plus_conv(a, b, 12)[1] == 2 + 3.5 * (9 / 7) + 2 * (9 / 5)
    assert min_plus_conv(a, b, 12.5)[1] == 2 + 3.5 * (9 / 7) + 2.5 * (9 / 5)


def test_max_plus_conv_1():
    a = PLF([Point(0, 2), Point(5, 4.5)])
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    assert max_plus_conv(a, b, 0)[1] == 2
    assert max_plus_conv(a, b, 0.5)[1] == 2.25
    assert max_plus_conv(a, b, 1)[1] == 2.5
    assert max_plus_conv(a, b, 1.5)[1] == 2.75
    assert max_plus_conv(a, b, 2)[1] == 3
    assert max_plus_conv(a, b, 2.5)[1] == 3.25
    assert max_plus_conv(a, b, 3)[1] == 3.5


def test_min_plus_deconv_1():
    a = PLF([Point(0, 2), Point(12, 5)])  # slope 0.25
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    assert min_plus_deconv(a, b, 0)[1] == 2.25
    assert min_plus_deconv(a, b, 1)[1] == 2.5
    assert min_plus_deconv(a, b, 2)[1] == 2.75
    assert min_plus_deconv(a, b, 3)[1] == 3


def test_max_plus_deconv_1():
    a = PLF([Point(0, 2), Point(12, 5)])  # slope 0.25
    b = PLF(
        [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 1), Point(4, 2), Point(5, 2)]
    )
    assert max_plus_deconv(a, b, 0)[1] == 1
    assert max_plus_deconv(a, b, 1)[1] == 1.25
    assert max_plus_deconv(a, b, 2)[1] == 1.5
    assert max_plus_deconv(a, b, 3)[1] == 1.75
