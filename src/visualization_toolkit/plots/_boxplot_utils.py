"""Helper functions for plotting boxplot."""

from typing import Sequence

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch


def is_broken(y_limits: Sequence) -> bool:
    """
    Use the limits to check if the axle is broken.
    Parameters:
       y_limits (Sequence): Sequence of (min, max) pairs.

    Returns:
        bool: True if the axle is broken, False otherwise.
    """
    return y_limits is not None and len(y_limits) >= 2


def check_y_limits(y_limits: Sequence) -> None:
    """
    Validate the y_limits parameter.
    Parameters:
       y_limits: Sequence of (min, max) pairs.
    """
    if y_limits is not None:
        if not all(
            isinstance(lim, (tuple, list)) and len(lim) == 2 for lim in y_limits
        ):
            raise ValueError(
                "y_limits must be a sequence of (min, max) tuples, "
                "e.g. y_limits=((1e-2, 1e-1),) or "
                "y_limits=((1e-3, 1e-2), (1e1, 1e2))"
            )


def create_axes(
    y_limits: Sequence,
    height_ratios: tuple,
    fig_size: tuple,
    ax: matplotlib.axes.Axes | None = None,
):
    """
    Create the axes for the boxplot.

    Parameters:
        y_limits (Sequence): Sequence of (min, max) pairs ordered bottom-to-top.
            One pair - single axis with that ylim.
            Two or more pairs - broken axis with one break per adjacent pair.
        height_ratios (tuple): Height ratios for the axes, ordered top-to-bottom
            (matching matplotlib's gridspec convention). Must have the same length
            as y_limits when a broken axis is used; otherwise equal ratios are used.
        fig_size (tuple): Size of the figure.
        ax (matplotlib.axes.Axes | None): Ax to plot on. Ignored when a broken axis
            is required (y_limits has two or more pairs).
    Returns:
        fig, axes: Figure and tuple of axes ordered top-to-bottom.
    """
    check_y_limits(y_limits)
    n = len(y_limits) if y_limits is not None else 0

    if n < 2:
        if ax is None:
            fig, ax_main = plt.subplots(figsize=fig_size)
        else:
            fig = ax.figure
            ax_main = ax
        if n == 1:
            ax_main.set_ylim(y_limits[0])
        return fig, (ax_main,)

    # n >= 2: create n subplots with n-1 breaks.
    # y_limits is ordered bottom-to-top; axes from subplots are top-to-bottom,
    # so axes[i] gets y_limits[n - 1 - i].
    ratios = height_ratios if len(height_ratios) == n else [1] * n
    fig, axes = plt.subplots(
        n,
        1,
        sharex=True,
        figsize=fig_size,
        layout="constrained",
        gridspec_kw={"height_ratios": ratios},
    )
    fig.get_layout_engine().set(hspace=0.05)
    for i, ax_ in enumerate(axes):
        lim = y_limits[n - 1 - i]
        if lim is None:
            raise ValueError(
                f"y_limits[{n - 1 - i}] is None; all limits must be (min, max) tuples"
            )
        ax_.set_ylim(lim)

    for i in range(n - 1):
        _draw_axis_break(axes[i], axes[i + 1])

    return fig, tuple(axes)


def get_x_levels(data: pd.DataFrame, x: str) -> list:
    """
    Get the unique values of a column as list.
    """
    if x is None:
        return [None]
    x_levels = data[x].unique()
    x_levels.sort()
    return x_levels


def add_legend(
    ax: matplotlib.axes.Axes,
    styles: dict,
    hue_levels: list,
    fontsize: float,
    ncol: int | None = None,
    bbox_to_anchor: tuple = (0.5, -0.15),
) -> None:
    """
    Add a legend to the figure below the x-axis label.

    Parameters:
        ax (matplotlib.axes.Axes): The main (bottom) axes.
        styles (dict): A dictionary of styles for each hue level.
        hue_levels (list): A list of hue levels.
        fontsize (float): The font size for the legend.
        ncol (int): The number of columns for the legend.
            len(hue_levels) will be set by default.
        bbox_to_anchor (tuple): Position of the legend anchor in axes coordinates.
            Defaults to (0.5, -0.15).
    """
    legend_handles = []
    if ncol is None:
        ncol = len(hue_levels)

    for hue_val in hue_levels:
        style = styles.get(hue_val, {})

        boxprops = style.get("boxprops", {})
        patch = Patch(
            facecolor=boxprops.get("facecolor", "none"),
            edgecolor=boxprops.get("edgecolor", "black"),
            hatch=boxprops.get("hatch", None),
            label=str(hue_val),
        )
        legend_handles.append(patch)

    ax.legend(
        handles=legend_handles,
        fontsize=fontsize,
        loc="upper center",
        bbox_to_anchor=bbox_to_anchor,
        ncol=ncol,
    )


def _draw_axis_break(ax_top, ax_bottom, d=0.5, **kwargs):
    """
    Draw diagonal break markers between two adjacent axes.

    Adds a pair of diagonal slash markers — one at the bottom edge of ax_top
    and one at the top edge of ax_bottom — to visually indicate a discontinuity
    in the Y axis.

    Parameters:
        ax_top(matplotlib.axes.Axes): The upper axis.
        ax_bottom(matplotlib.axes.Axes): The lower axis.
        d(float): Controls the slope of the diagonal marker. Larger values
            produce a steeper slash. Defaults to 0.5.
        **kwargs: Additional keyword arguments to override default marker properties.
                  Common options include: color, markersize, markeredgewidth (mew), etc.

    Returns:
      None: Modifies the axes in-place by adding break markers.
    """
    default_kwargs = {
        "color": "k",
        "clip_on": False,
        "marker": [(-1, -d), (1, d)],
        "markersize": 12,
        "linestyle": "none",
        "mec": "k",
        "mew": 1,
    }
    default_kwargs.update(kwargs)
    ax_top.plot([0, 1], [0, 0], transform=ax_top.transAxes, **default_kwargs)
    ax_bottom.plot([0, 1], [1, 1], transform=ax_bottom.transAxes, **default_kwargs)
