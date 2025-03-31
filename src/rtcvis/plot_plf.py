import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

from rtcvis.plf import PLF
from rtcvis.point import Point
from rtcvis.conv import ConvType, conv, min_plus_conv


def plot_plf(a: PLF, b: PLF):
    fig, ax = plt.subplots()
    ax.set_aspect("equal", adjustable="box")

    # Make room for bottom slider
    fig.subplots_adjust(bottom=0.25)

    # Create bottom slider
    axdeltax = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    deltax_slider = Slider(ax=axdeltax, label="delta_x", valmin=0, valmax=10, valinit=0)

    # plot a
    x = [p.x for p in a.points]
    y = [p.y for p in a.points]
    ax.plot(x, y)

    # plot b
    b = b.transformed(True, 0)
    x = [p.x for p in b.points]
    y = [p.y for p in b.points]
    (graph_b,) = ax.plot(x, y)

    # plot conv at x
    initial_x = 0
    s, res = min_plus_conv(a, b, delta_x=initial_x)
    x = [p.x for p in s.points]
    y = [p.y for p in s.points]
    (graph_sum,) = ax.plot(x, y)

    # add marker for conv result
    # (graph_marker,) = ax.plot([initial_x], res, marker="s")

    # Slider update function
    def update(val):
        # Update sum function
        s, res = min_plus_conv(a, b, delta_x=val)
        x = [p.x for p in s.points]
        y = [p.y for p in s.points]
        graph_sum.set_xdata(x)
        graph_sum.set_ydata(y)

        # # Update minconv marker
        # graph_marker.set_xdata([s.min])
        # graph_marker.set_ydata([min_y])

        # Update function b
        b = b.transformed(False, val)
        x = [p.x for p in b.points]
        graph_b.set_xdata(x)
        fig.canvas.draw_idle()

    # register the slider
    deltax_slider.on_changed(update)

    return fig


if __name__ == "__main__":
    a = PLF([Point(0, 0), (0.1, 0.0), (0.5, 0.4)])
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    c = conv(a, b, ConvType.MIN_PLUS_CONV)
    fig = plot_plf(a, b)
    plt.show()
