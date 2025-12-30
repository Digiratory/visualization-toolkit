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
    estimator: str = "mean",
    errorbar_type: str = "p",
    errorbar_data: tuple = (5, 95),
    styles: dict = None,
    logy: bool = True,
    ylim: tuple = None,
    xlabel: str = "С/Ш, дБ",
    ylabel: str = "СКО",
    title: str = "Зависимость СКО от уровня шума",
    axes_fontsize: int = 22,
    title_fontsize: int = 24,
    ax: matplotlib.axes.Axes = None,
):
    """
    Plot mean squared error (MSE) with error bars as a function of a noise-related variable.

    The function groups the input data by the `hue` column, aggregates metric values
    using the specified estimator and error bar definition, and visualizes the result
    using Matplotlib error bar plots.

    Parameters:
        data(pandas.DataFrame): Input data containing experimental results.
            Must include columns specified by `x`, `y`, and `hue`.

        x(str): Name of the column used as the independent variable
            (e.g., noise level or signal-to-noise ratio).

        y(str): Name of the column containing the error metric to be plotted
            (e.g., mean squared error).

        hue(str): Name of the column used to group the data into separate curves
            (e.g., different models or methods).

        estimator(str): Aggregation function used to compute the central
            tendency of `y` for each value of `x` (e.g., `"mean"`, `"median"`).

        errorbar_type(str): Type of error bars to compute.
            Passed to the `aggregate` function (e.g., `"p"` for percentiles).

        errorbar_data(tuple): Parameters defining the error bars.
            For percentile-based intervals, specifies the lower and upper percentiles.

        styles(dict or None): Optional mapping from group labels to Matplotlib style
            dictionaries (e.g., line style, marker, color).

        logy(bool): If True, use a logarithmic scale for the y-axis.

        ylim(tuple or None): Optional limits for the y-axis.

        xlabel(str): Label for the x-axis.

        ylabel(str): Label for the y-axis.

        title(str): Plot title.

        axes_fontsize(int): Font size for axis labels and legend.

        title_fontsize(int): Font size for the plot title.

        ax(matplotlib.axes.Axes or None): Existing Matplotlib axes to draw on.
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
            capsize=5,
            linewidth=3,
            **style,
        )

    if logy:
        plt.yscale("log")
    if ylim:
        ax.set_ylim(ylim)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=axes_fontsize)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=axes_fontsize)
    if title:
        ax.set_title(title, fontsize=title_fontsize)
    ax.legend(fontsize=axes_fontsize)
    ax.grid(True)
    return ax
