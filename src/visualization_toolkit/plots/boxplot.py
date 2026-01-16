"Boxplot plotting"

from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

from visualization_toolkit.plots._broken_axis import _draw_axis_break


def boxplot(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: str | None = None,
    styles: dict = None,
    broken: bool = False,
    logy: bool = True,
    bottom_ylim=None,
    top_ylim=None,
    xlabel: str = None,
    ylabel: str = None,
    title: str = None,
    height_ratios=(1, 2),
    axes_fontsize: int = 20,
    title_fontsize: int = 22,
    fig_size: tuple = (12, 8),
    ax=None,
    **kwargs,
):
    """
    Boxplot with optional broken Y axis.

    Parameters:
        data (pd.DataFrame): Input data containing experimental values.
                             Must include columns specified by x and y, and hue if used.
        x (str): Column name used as the categorical X-axis.
        y (str): Column name with values to plot as boxplots.
        hue (str | None, optional): Column name for additional grouping within X categories.
        styles (dict, optional): Dictionary of styles for different hue levels,
                                 passed to ax.boxplot.
        broken (bool, optional): If True, use a broken Y-axis with two subplots.
        logy (bool, optional): If True, use a logarithmic scale for Y-axis.
        bottom_ylim (tuple, optional): Y-axis limits for the bottom axis when broken=True.
        top_ylim (tuple, optional): Y-axis limits for the top axis when broken=True.
        xlabel (str, optional): Label for the X-axis.
        ylabel (str, optional): Label for the Y-axis.
        title (str, optional): Plot title.
        height_ratios (tuple, optional): Relative heights of top and bottom axes for broken=True.
        axes_fontsize (int, optional): Font size for axis labels and ticks.
        title_fontsize (int, optional): Font size for the title.
        fig_size (tuple, optional): Figure size (width, height) in inches.
        ax (matplotlib.axes.Axes, optional): Existing axes to plot on. Creates new figure if None.

    Returns:
        Tuple if broken=True, else single Axes.
        fig (matplotlib.figure.Figure): Figure object containing the plot.
        ax (matplotlib.axes.Axes or tuple of Axes): Axes object(s).
    """
    if styles is None:
        styles = {}
    if broken:
        if bottom_ylim is None or top_ylim is None:
            raise ValueError("bottom_ylim and top_ylim required if broken=True")
        fig, (ax_top, ax_bottom) = plt.subplots(
            2,
            1,
            sharex=True,
            figsize=fig_size,
            gridspec_kw={
                "height_ratios": height_ratios,
                "hspace": 0.05,
            },
        )
        axes = (ax_top, ax_bottom)
        ax_main = ax_bottom
        _draw_axis_break(ax_top, ax_bottom)
        ax_bottom.set_ylim(bottom_ylim)
        ax_top.set_ylim(top_ylim)
    else:
        if ax is None:
            fig, ax_main = plt.subplots(figsize=fig_size)
        else:
            fig = ax.figure
            ax_main = ax
        axes = (ax_main,)

    x_levels = data[x].unique()
    x_levels.sort()

    if hue is None:
        hue_levels = [None]
    else:
        hue_levels = data[hue].unique()
        hue_levels.sort()

    n_groups = len(x_levels)
    n_hue = len(hue_levels)
    base_positions = np.arange(1, n_groups + 1)

    for ax_ in axes:
        plot_box_on_axis(
            data,
            x,
            y,
            hue,
            hue_levels,
            n_hue,
            base_positions,
            x_levels,
            styles,
            ax_,
            **kwargs,
        )
        if logy:
            ax_.set_yscale("log")
        ax_.grid(True)
        ax_.tick_params(axis="both", labelsize=axes_fontsize - 4)

    ax_main.set_xticks(base_positions)
    ax_main.set_xticklabels(x_levels)
    if xlabel is not None:
        ax_main.set_xlabel(xlabel, fontsize=axes_fontsize)
    if ylabel is not None:
        ax_main.set_ylabel(ylabel, fontsize=axes_fontsize)
    if title is not None and broken:
        ax_top.set_title(title, fontsize=title_fontsize)
    elif title is not None:
        ax_main.set_title(title, fontsize=title_fontsize)

    if hue is not None and styles:
        legend_handles = []

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

        fig.legend(
            handles=legend_handles,
            fontsize=axes_fontsize - 4,
            loc="lower center",
            ncol=n_hue,
        )
    return fig, axes if broken else ax_main


def plot_box_on_axis(
    data,
    x: str,
    y: str,
    hue: str,
    hue_levels: list,
    n_hue: int,
    base_positions: Any,
    x_levels: Any,
    styles: dict,
    ax: matplotlib.axes.Axes,
    **kwargs,
):
    """
    Plot boxplots on a given axis.

    Parameters
        data (pd.DataFrame): Input data containing experimental values.
        x (str): Column name used as the categorical X-axis.
        y (str): Column name with values to plot as boxplots.
        hue (str or None): Column name for additional grouping within X categories.
        hue_levels (list): Unique values of the hue variable.
        n_hue (int): Number of unique hue levels.
        base_positions (array-like): Positions for each X category on the X-axis.
        x_levels (array-like): Unique values of the X variable.
        styles (dict): Dictionary of styles for each hue value, passed to ax.boxplot.
        ax (matplotlib.axes.Axes): Axis object on which to draw the boxplots.
    """
    width = 0.8 / max(1, n_hue)
    for i, hue_val in enumerate(hue_levels):
        offset = (i - (n_hue - 1) / 2) * width

        for j, x_val in enumerate(x_levels):
            mask = data[x] == x_val
            if hue is not None:
                mask &= data[hue] == hue_val

            values = data.loc[mask, y].values
            if len(values) == 0:
                continue

            ax.boxplot(
                values,
                positions=[base_positions[j] + offset],
                widths=width * 0.9,
                **kwargs,
                **(styles.get(hue_val, {}) if styles else {}),
            )
