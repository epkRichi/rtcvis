import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.colors as mcolors
import numpy as np

from rtcvis.plf import PLF
from rtcvis.point import Point
from rtcvis.conv import ConvType, conv, conv_at_x


def plot_conv(a: PLF, b: PLF):
    assert a.x_start == 0 and b.x_start == 0 and a.x_end == b.x_end

    color_a = mcolors.TABLEAU_COLORS["tab:olive"]
    color_b = mcolors.TABLEAU_COLORS["tab:orange"]
    color_sum = mcolors.TABLEAU_COLORS["tab:purple"]
    color_result = mcolors.TABLEAU_COLORS["tab:gray"]

    fig, ax = plt.subplots()
    ax.set_aspect("equal", adjustable="box")

    # compute initial convolution result
    initial_x = 0
    conv_type = ConvType.MIN_PLUS_CONV
    conv_result = conv_at_x(a, b, initial_x, conv_type)

    # Make room for bottom slider
    fig.subplots_adjust(bottom=0.25)

    # Create bottom slider
    axdeltax = fig.add_axes((0.25, 0.1, 0.65, 0.03))
    deltax_slider = Slider(
        ax=axdeltax, label="delta_x", valmin=0, valmax=a.x_end, valinit=initial_x
    )

    # plot transformed a
    (graph_a,) = ax.plot(
        conv_result.transformed_a.x,
        conv_result.transformed_a.y,
        label="transformed a",
        color=color_a,
    )

    # plot b
    ax.plot(b.x, b.y, label="b", color=color_b)

    # plot convolution sum
    (graph_sum,) = ax.plot(
        conv_result.sum.x, conv_result.sum.y, label="sum", color=color_sum
    )

    # add marker for conv result
    (graph_marker,) = ax.plot(
        [conv_result.result.x],
        [conv_result.result.y],
        marker=".",
        label="sum minimum",
        color=graph_sum.get_color(),
    )

    # plot full result
    # conv_plf = conv(a, b, conv_type, 0, a.x_end)
    # ax.plot(conv_plf.x, conv_plf.y, label="full result", color=color_result)

    # Slider update function
    def update(val):
        # Recompute convolution
        conv_result = conv_at_x(a, b, val, conv_type)

        # Update transformed a
        graph_a.set_xdata(conv_result.transformed_a.x)
        graph_a.set_ydata(
            conv_result.transformed_a.y
        )  # y doesn't really change but hey
        fig.canvas.draw_idle()

        # Update sum PLF
        graph_sum.set_xdata(conv_result.sum.x)
        graph_sum.set_ydata(conv_result.sum.y)

        # Update minconv marker
        graph_marker.set_xdata([conv_result.result.x])
        graph_marker.set_ydata([conv_result.result.y])

    # register the slider
    deltax_slider.on_changed(update)

    # add legend
    ax.legend(loc="upper left")

    plt.show()


if __name__ == "__main__":
    a = PLF([Point(0, 0), (1, 0), (5, 4)])
    b = PLF([(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2)])
    plot_conv(a, b)
