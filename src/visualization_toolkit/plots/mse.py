"""MSE plotting"""

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from ..core.aggregation import aggregate


def mseplot(
    data: pd.DataFrame,
    x: str = "snr",
    y: str = "mse",
    hue: str = "label",
    estimator: str = "median",
    errorbar_type: str = "p",
    errorbar_data: tuple = (5, 95),
    styles: dict | None = None,
    logy: bool = True,
    y_lim: tuple | None = None,
    x_label: str = "С/Ш, дБ",
    y_label: str = "СКО",
    title: str = "Зависимость СКО от уровня шума",
    axes_fontsize: int = 22,
    title_fontsize: int = 24,
    ax: matplotlib.axes.Axes | None = None,
    **kwargs,
):
    """
    Plot mean squared error (MSE) with error bars as a function of a noise-related variable.

    The function groups the input data by the `hue` column, aggregates metric values
    using the specified estimator and error bar definition, and visualizes the result
    using Matplotlib error bar plots.

    Parameters:
        data(pandas.DataFrame): Input data containing experimental results.
            Must include columns specified by `x`, `y`, and `hue`.

        x(str, default="snr"): Name of the column used as the independent variable
            (e.g., noise level or signal-to-noise ratio).

        y(str, default="mse"): Name of the column containing the error metric to be plotted
            (e.g., mean squared error).

        hue(str, default="label"): Name of the column used to group the data into separate curves
            (e.g., different models or methods).

        estimator(str, default="median"): Aggregation function used to compute the central
            tendency of `y` for each value of `x` (e.g., `"mean"`, `"median"`).

        errorbar_type(str, default="p"): Type of error bars to compute.
            Passed to the `aggregate` function (e.g., `"p"` for percentiles).

        errorbar_data(tuple, default=(5, 95)): Parameters defining the error bars.
            For percentile-based intervals, specifies the lower and upper percentiles.

        styles(dict or None, default=None): Optional mapping from group labels to Matplotlib style
            dictionaries (e.g., line style, marker, color).

        logy(bool, default=True): If True, use a logarithmic scale for the y-axis.

        y_lim(tuple or None, default=None): Optional limits for the y-axis.

        x_label(str): Label for the x-axis.

        y_label(str): Label for the y-axis.

        title(str): Plot title.

        axes_fontsize(int, default=22): Font size for axis labels and legend.

        title_fontsize(int, default=24): Font size for the plot title.

        ax(matplotlib.axes.Axes or None, default=None): Existing Matplotlib axes to draw on.
            If None, a new figure and axes are created.

    Returns:
        matplotlib.axes.Axes: The axes object containing the plot.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))

    for label in data[hue].unique():
        mse_mean, mse_err = aggregate(
            data[(data[hue] == label)],
            x,
            y,
            estimator=estimator,
            errorbar_type=errorbar_type,
            errorbar_data=errorbar_data,
        )
        style = styles.get(label, {}) if styles else {}

        ax.errorbar(
            data[x].unique(),
            mse_mean,
            yerr=mse_err,
            label=label,
            **style,
            **kwargs,
        )

    if logy:
        plt.yscale("log")
    if y_lim:
        ax.set_ylim(y_lim)
    if x_label:
        ax.set_xlabel(x_label, fontsize=axes_fontsize)
    if y_label:
        ax.set_ylabel(y_label, fontsize=axes_fontsize)
    if title:
        ax.set_title(title, fontsize=title_fontsize)
    ax.legend(fontsize=axes_fontsize)
    ax.grid(True)
    return ax
