from rtcvis import *


if __name__ == "__main__":
    a = PLF([Point(0, 0), (1, 0), (5, 4)])
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    plot_plfs([a, b])

    plot_conv(a, b, ConvType.MIN_PLUS_CONV, True)
    plot_conv(a, b, ConvType.MIN_PLUS_DECONV, True)
    plot_conv(a, b, ConvType.MAX_PLUS_CONV, True)
    plot_conv(a, b, ConvType.MAX_PLUS_DECONV, True)
