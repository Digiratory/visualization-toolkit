"Boxplot plotting"

from typing import Any, Callable, Sequence, Tuple

import matplotlib
import numpy as np
import pandas as pd

from visualization_toolkit.plots._boxplot_utils import (
    add_legend,
    create_axes,
    get_x_levels,
    is_broken,
)
from visualization_toolkit.plots._significance_boxplot import add_significance


def boxplot(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: str | None = None,
    styles: dict | None = None,
    y_limits: Sequence[Tuple[float, float]] | None = None,
    significance_fn: Callable | None = None,
    significance_levels: dict[float, str] | None = None,
    logy: bool = False,
    x_label: str | None = None,
    y_label: str | None = None,
    title: str | None = None,
    height_ratios: Tuple = (1, 2),
    axes_fontsize: int = 20,
    title_fontsize: int = 22,
    fig_size: tuple = (12, 8),
    ax: matplotlib.axes.Axes | None = None,
    legend_ncol: int | None = None,
    legend_bbox_to_anchor: tuple = (0.5, -0.15),
    show_median_text: bool = False,
    show_mean_text: bool = False,
    median_mean_fontsize: int | None = None,
    **kwargs,
):
    """
    Boxplot with optional broken Y axis.
    Steps:
    - validate_inputs
    - create_axes
    - compute_layout
    - draw_boxes
    - configure_axes
    - draw_legend
    - draw_significance

    Parameters:
        data (pd.DataFrame): Input data containing experimental values.
                             Must include columns specified by x and y, and hue if used.
        x (str): Column name used as the categorical X-axis.
        y (str): Column name with values to plot as boxplots.
        hue (str | None, optional): Column name for additional grouping within X categories.
        styles (dict, optional): Dictionary of styles for different hue levels,
                                 passed to ax.boxplot.
        y_limits (Sequence[Tuple[float, float]], optional): Y-axis limits ordered
                            bottom-to-top. One tuple - single axis; two or more tuples -
                            broken axis with one break per adjacent pair.
        x_label (str, optional): Label for the X-axis.
        y_label (str, optional): Label for the Y-axis.
        title (str, optional): Plot title.
        height_ratios (tuple, optional): Relative heights of the subplot panels,
                            ordered top-to-bottom (matplotlib gridspec convention).
                            Must have the same length as y_limits when a broken axis
                            is used; otherwise equal ratios are applied.
        axes_fontsize (int, optional): Font size for axis labels and ticks.
        title_fontsize (int, optional): Font size for the title.
        fig_size (tuple, optional): Figure size (width, height) in inches.
        ax (matplotlib.axes.Axes, optional): Existing axes to plot on. Creates new figure if None.
        legend_ncol (int): The number of columns for the legend.
            len(hue_levels) will be set by default.
        legend_bbox_to_anchor (tuple): Position of the legend anchor in axes coordinates.
            Defaults to (0.5, -0.15).
        show_median_text (bool, optional): If True, display the median value above each box.
            Defaults to False.
        show_mean_text (bool, optional): If True, display the mean value above each box.
            Defaults to False.
        median_mean_fontsize (int, optional): Font size for the median/mean labels.
            If both show_median_text and show_mean_text are True, the labels are stacked with
            median on top and mean below. Defaults to axes_fontsize - 6.

    Returns:
        fig (matplotlib.figure.Figure): Figure object containing the plot.
        axes (tuple[matplotlib.axes.Axes, ...]): Tuple of axes ordered top-to-bottom.
            Contains one element when y_limits has fewer than two pairs,
            and N elements when y_limits has N pairs (broken axis).
    """

    if styles is None:
        styles = {}
    if (significance_fn is not None) and (is_broken(y_limits)):
        raise NotImplementedError(
            "Significance annotations are not supported when using a broken y-axis "
            "because bracket/label placement can be ambiguous across split panels. "
            "Workaround: disable significance_fn or use a single, non-broken y-axis."
        )

    fig, axes = create_axes(
        y_limits=y_limits, height_ratios=height_ratios, fig_size=fig_size, ax=ax
    )
    ax_top = axes[0]
    ax_main = axes[-1]
    x_levels = get_x_levels(data, x)
    hue_levels = get_x_levels(data, hue)
    base_positions = np.arange(1, len(x_levels) + 1)

    for ax_ in axes:
        plot_box_on_axis(
            data,
            x,
            y,
            hue,
            hue_levels,
            base_positions,
            x_levels,
            styles,
            ax_,
            show_median_text=show_median_text,
            show_mean_text=show_mean_text,
            median_mean_fontsize=(
                median_mean_fontsize
                if median_mean_fontsize is not None
                else axes_fontsize - 6
            ),
            **kwargs,
        )
        if logy:
            ax_.set_yscale("log")
        ax_.grid(True)
        ax_.tick_params(axis="both", labelsize=axes_fontsize - 4)

    ax_main.set_xticks(base_positions)
    ax_main.set_xticklabels(x_levels)
    ax_main.set_xlabel(x_label, fontsize=axes_fontsize)
    ax_main.set_ylabel(y_label, fontsize=axes_fontsize)
    ax_top.set_title(title, fontsize=title_fontsize)

    if hue is not None:
        add_legend(
            ax_main,
            styles,
            hue_levels,
            axes_fontsize - 4,
            ncol=legend_ncol,
            bbox_to_anchor=legend_bbox_to_anchor,
        )

    if significance_fn is None:
        return fig, axes

    add_significance(
        ax=ax_top,
        data=data,
        significance_fn=significance_fn,
        x=x,
        y=y,
        hue=hue,
        hue_levels=hue_levels,
        x_levels=x_levels,
        base_positions=base_positions,
        levels=significance_levels,
    )
    return fig, axes


def plot_box_on_axis(
    data,
    x: str,
    y: str,
    hue: str | None,
    hue_levels: list,
    base_positions: Any,
    x_levels: Any,
    styles: dict,
    ax: matplotlib.axes.Axes,
    show_median_text: bool = False,
    show_mean_text: bool = False,
    median_mean_fontsize: int = 10,
    **kwargs,
):
    """
    Plot boxplots on a given axis.

    Parameters
    ----------
    data : pd.DataFrame
        Input data containing experimental values.
    x : str
        Column name used as the categorical X-axis.
    y : str
        Column name with values to plot as boxplots.
    hue : str | None
        Column name for additional grouping within X categories.
    hue_levels : list
        Unique values of the hue variable.
    base_positions : array-like
        Positions for each X category on the X-axis.
    x_levels : array-like
        Unique values of the X variable.
    styles : dict
        Dictionary of styles for each hue value, passed to ax.boxplot.
    ax : matplotlib.axes.Axes
        Axis object on which to draw the boxplots.
    show_median_text : bool, default=False
        If True, show the median value above the box.
    show_mean_text : bool, default=False
        If True, show the mean value above the box.
        If both show_median_text and show_mean_text are True, labels are stacked:
        median on top, mean below.
    median_mean_fontsize : int, default=10
        Font size for the median/mean labels.
    """
    n_hue = len(hue_levels)
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

            pos = base_positions[j] + offset
            ax.boxplot(
                values,
                positions=[pos],
                widths=width * 0.9,
                **kwargs,
                **(styles.get(hue_val, {}) if styles else {}),
            )

            if show_median_text or show_mean_text:
                q3 = np.percentile(values, 75)
                if show_median_text and show_mean_text:
                    label = f"{np.median(values):.3g}\n{np.mean(values):.3g}"
                elif show_median_text:
                    label = f"{np.median(values):.3g}"
                else:
                    label = f"{np.mean(values):.3g}"
                ax.text(
                    pos,
                    q3 * 1.05,
                    label,
                    ha="center",
                    va="bottom",
                    fontsize=median_mean_fontsize,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 1},
                )
