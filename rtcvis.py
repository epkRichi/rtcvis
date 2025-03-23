import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider


def show_min_plus(a, b):
    fig, ax = plt.subplots()

    ax.set_aspect("equal", adjustable="box")

    # Make room for bottom slider
    fig.subplots_adjust(bottom=0.25)

    # Create bottom slider
    axdeltax = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    deltax_slider = Slider(
        ax=axdeltax,
        label="delta_x",
        valmin=0,
        valmax=10,
        valinit=0
    )

    # compute the x values
    sampling_rate = 100
    x = np.linspace(0, 10, 10 * sampling_rate)

    # plot function a
    y_a = a(x)
    ax.plot(x, y_a)

    # plot function b
    y_b = b(x)
    graph_b, = ax.plot(-x, y_b)

    initial_sum = y_a[0] + y_b[0]

    # plot sum of a and b
    graph_sum, = ax.plot([0], initial_sum)

    # add marker for minconv result
    graph_marker, = ax.plot([0], initial_sum, marker="s")

    # Slider update function
    def update(val):
        # Compute result of minconv
        delta_idx = int(sampling_rate * val) + 1 # +1 to prevent empty frames
        a_frame = y_a[:delta_idx]
        b_frame = np.flip(y_b[:delta_idx])
        sum_frame = a_frame + b_frame
        min_idx = np.argmin(sum_frame)
        min_x = x[min_idx]
        min_y = sum_frame[min_idx]

        # Update sum function
        graph_sum.set_xdata(x[:delta_idx])
        graph_sum.set_ydata(sum_frame)

        # Update minconv marker
        graph_marker.set_xdata([min_x])
        graph_marker.set_ydata([min_y])

        # Update function b
        graph_b.set_xdata(-x+val)
        fig.canvas.draw_idle()

    # register the slider
    deltax_slider.on_changed(update)

    plt.show()


def a(x):
    return x

def b(x):
    return x + 1

def main():
    show_min_plus(a, b)

if __name__ == "__main__":
    main()
