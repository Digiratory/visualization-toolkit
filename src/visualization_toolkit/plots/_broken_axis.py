"""Add broken axis to a matplotlib figure."""


def _draw_axis_break(ax_top, ax_bottom, d=0.015):
    """
    Draw a broken axis between two axes.

    Parameters:
        ax_top(matplotlib.axes.Axes): The top axis.
        ax_bottom(matplotlib.axes.Axes): The bottom axis.
        d(float): The distance from the top axis to the bottom.

    Returns:
      None
    """
    kwargs = {"color": "k", "clip_on": False}
    ax_top.plot((-d, +d), (-d, +d), transform=ax_top.transAxes, **kwargs)
    ax_top.plot((1 - d, 1 + d), (-d, +d), transform=ax_top.transAxes, **kwargs)

    ax_bottom.plot((-d, +d), (1 - d, 1 + d), transform=ax_bottom.transAxes, **kwargs)
    ax_bottom.plot(
        (1 - d, 1 + d), (1 - d, 1 + d), transform=ax_bottom.transAxes, **kwargs
    )
