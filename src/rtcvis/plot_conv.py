import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
import matplotlib.colors as mcolors

from rtcvis.plf import PLF
from rtcvis.conv import ConvType, conv, conv_at_x, LAMBDA, DELTA


class ConvProperties:
    def __init__(self, a: PLF, b: PLF, conv_type: ConvType):
        """Computes several properties needed for plotting convolutions.

        Computes the min and max values for the slider, x axis and y axis as well as
        the result of the convolution.

        Args:
            a (PLF): PLF a.
            b (PLF): PLF b.
            conv_type (ConvType): The type of convolution.
        """
        # allow computing the convolution for all x>=0 upto the point where a and b no
        # longer overlap
        PADDING = 0.5
        is_deconv = conv_type in (ConvType.MAX_PLUS_DECONV, ConvType.MIN_PLUS_DECONV)
        if is_deconv:
            min_deconv_result = conv(
                a=a, b=b, conv_type=ConvType.MIN_PLUS_DECONV, start=0
            )
            max_deconv_result = conv(
                a=a, b=b, conv_type=ConvType.MAX_PLUS_DECONV, start=0
            )
            conv_min_x = (a.x_start - a.x_end) + b.x_start
            conv_max_x = max(a.x_end, b.x_end)
            conv_min_y = max_deconv_result.min.y
            conv_max_y = min_deconv_result.max.y
            self.slider_max = a.x_end - b.x_start
            self.result = (
                min_deconv_result
                if conv_type == ConvType.MIN_PLUS_DECONV
                else max_deconv_result
            )
        else:
            min_conv_result = conv(a=a, b=b, conv_type=ConvType.MIN_PLUS_CONV, start=0)
            max_conv_result = conv(a=a, b=b, conv_type=ConvType.MAX_PLUS_CONV, start=0)
            conv_min_x = min(-a.x_end, b.x_start)
            conv_max_x = b.x_end + (a.x_end - a.x_start)
            conv_min_y = min_conv_result.min.y
            conv_max_y = max_conv_result.max.y
            self.slider_max = b.x_end + a.x_end
            self.result = (
                min_conv_result
                if conv_type == ConvType.MIN_PLUS_CONV
                else max_conv_result
            )
        ab_min_y = min(a.min.y, b.min.y)
        ab_max_y = max(a.max.y, b.max.y)
        self.slider_min = 0
        self.min_x = conv_min_x - PADDING
        self.max_x = conv_max_x + PADDING
        self.min_y = min(ab_min_y, conv_min_y) - PADDING
        self.max_y = max(ab_max_y, conv_max_y) + PADDING


def plot_conv(a: PLF, b: PLF, conv_type: ConvType):
    """Plots a convolution using matplotlib.

    The plot is interactive: The user can enter the delta for which to compute the
    convolution using a slider. The plot will show the original PLF a, the transformed
    PLF a, PLF b, the sum/difference of those two and the full result of the
    convolution. All functions can individually be toggled in the legend.

    Args:
        a (PLF): PLF a.
        b (PLF): PLF b.
        conv_type (ConvType): The type of convolution.
    """
    conv_properties = ConvProperties(a=a, b=b, conv_type=conv_type)

    color_a = mcolors.TABLEAU_COLORS["tab:cyan"]
    color_trans_a = mcolors.TABLEAU_COLORS["tab:olive"]
    color_b = mcolors.TABLEAU_COLORS["tab:orange"]
    color_sum = mcolors.TABLEAU_COLORS["tab:purple"]
    color_result = mcolors.TABLEAU_COLORS["tab:gray"]
    colors = (color_a, color_trans_a, color_b, color_sum, color_result)

    fig, ax = plt.subplots()
    ax.set_aspect("equal", adjustable="box")

    # compute initial convolution result
    initial_x = 0
    conv_result = conv_at_x(a, b, initial_x, conv_type)

    # Make room for bottom slider
    fig.subplots_adjust(bottom=0.25)

    # Create bottom slider
    plot_pos = ax.get_position(True)
    axdeltax = fig.add_axes((plot_pos.x0, plot_pos.y0 - 0.12, plot_pos.width, 0.02))
    deltax_slider = Slider(
        ax=axdeltax,
        label=f"${DELTA}$",
        valmin=0,
        valmax=conv_properties.slider_max,
        valinit=initial_x,
        valfmt="%.2f",
    )

    # plot a (but hide it by default)
    (graph_a,) = ax.plot(a.x, a.y, label=conv_type.a_desc, color=color_a)
    graph_a.set_visible(False)

    # plot transformed a
    (graph_trans_a,) = ax.plot(
        conv_result.transformed_a.x,
        conv_result.transformed_a.y,
        label=conv_type.a_trans_desc,
        color=color_trans_a,
    )

    # plot b
    (graph_b,) = ax.plot(b.x, b.y, label=conv_type.b_desc, color=color_b)

    # plot convolution sum
    (graph_sum,) = ax.plot(
        conv_result.sum.x,
        conv_result.sum.y,
        label=conv_type.sum_desc,
        color=color_sum,
    )

    # add marker for conv result
    (graph_sum_marker,) = ax.plot(
        [conv_result.result.x],
        [conv_result.result.y],
        marker=".",
        color=color_sum,
    )

    # plot full result of convolution
    conv_plf = conv_properties.result
    (graph_result,) = ax.plot(
        conv_plf.x,
        conv_plf.y,
        label=conv_type.operator_desc,
        color=color_result,
    )
    # add marker for where we're currently at
    (graph_result_marker,) = ax.plot(
        [initial_x],
        [conv_plf(initial_x)],
        marker=".",
        color=color_result,
    )

    # Slider update function
    def slider_callback(val):
        # Recompute convolution
        conv_result = conv_at_x(a, b, val, conv_type)

        # Update transformed a
        graph_trans_a.set_xdata(conv_result.transformed_a.x)
        graph_trans_a.set_ydata(
            conv_result.transformed_a.y
        )  # y doesn't really change but hey

        # Update sum PLF
        graph_sum.set_xdata(conv_result.sum.x)
        graph_sum.set_ydata(conv_result.sum.y)

        # Update sum marker
        graph_sum_marker.set_xdata([conv_result.result.x])
        graph_sum_marker.set_ydata([conv_result.result.y])

        # update result marker
        graph_result_marker.set_xdata([val])
        graph_result_marker.set_ydata([conv_plf(val)])

        fig.canvas.draw_idle()

    # register the slider
    deltax_slider.on_changed(slider_callback)

    # create legend with check buttons for toggling the visibility
    rax = ax.inset_axes((0.0, 0.0, 0.12, 0.2))
    check = CheckButtons(
        ax=rax,
        labels=[
            conv_type.a_desc,
            conv_type.a_trans_desc,
            conv_type.b_desc,
            conv_type.sum_desc,
            conv_type.operator_desc,
        ],
        actives=[
            graph_a.get_visible(),
            graph_trans_a.get_visible(),
            graph_b.get_visible(),
            graph_sum.get_visible(),
            graph_result.get_visible(),
        ],
        label_props={"color": colors},
        frame_props={"edgecolor": colors},
        check_props={"facecolor": colors},
    )

    # checkbox update function
    def check_callback(label: str | None):
        if label == conv_type.a_desc:
            graph_a.set_visible(not graph_a.get_visible())
        elif label == conv_type.a_trans_desc:
            graph_trans_a.set_visible(not graph_trans_a.get_visible())
        elif label == conv_type.b_desc:
            graph_b.set_visible(not graph_b.get_visible())
        elif label == conv_type.sum_desc:
            graph_sum_marker.set_visible(not graph_sum.get_visible())
            graph_sum.set_visible(not graph_sum.get_visible())
        elif label == conv_type.operator_desc:
            graph_result_marker.set_visible(not graph_result.get_visible())
            graph_result.set_visible(not graph_result.get_visible())
        fig.canvas.draw_idle()

    # register the checkboxes
    check.on_clicked(check_callback)

    # set limits, title and xlabel
    ax.set_xlim(conv_properties.min_x, conv_properties.max_x)
    ax.set_ylim(conv_properties.min_y, conv_properties.max_y)
    ax.set_title(
        f"{conv_type}: ${conv_type.operator_desc[1:-1]} = {conv_type.full_desc[1:-1]}$"
    )
    ax.set_xlabel(f"${LAMBDA}$")

    plt.show()
