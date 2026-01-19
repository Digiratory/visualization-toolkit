"""Add broken axis to a matplotlib figure."""


def _draw_axis_break(ax_top, ax_bottom, d=0.5):
    """
    Draw a broken axis between two axes.

    Parameters:
        ax_top(matplotlib.axes.Axes): The top axis.
        ax_bottom(matplotlib.axes.Axes): The bottom axis.
        d(float): The distance from the top axis to the bottom.

    Returns:
      None
    """
    kwargs = {
        "color": "k",
        "clip_on": False,
        "marker": [(-1, -d), (1, d)],
        "markersize": 12,
        "linestyle": "none",
        "mec": "k",
        "mew": 1,
    }
    ax_top.plot([0, 1], [0, 0], transform=ax_top.transAxes, **kwargs)
    ax_bottom.plot([0, 1], [1, 1], transform=ax_bottom.transAxes, **kwargs)
