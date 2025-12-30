"""MSE plotting"""

import matplotlib.pyplot as plt

from ..core.aggregation import aggregate


def mseplot(
    data,
    *,
    x="snr",
    y="mse",
    hue="label",
    estimator="mean",
    errorbar=("p", (5, 95)),
    styles=None,
    logy=True,
    ylim=None,
    xlabel="С/Ш, дБ",
    ylabel="СКО",
    title="Зависимость СКО от уровня шума",
    axes_fontsize=22,
    title_fontsize=24,
    ax=None,
):
    """
    Plot mean MSE values with error bars as a function of a noise-related variable.

    The function groups data by the `hue` column, aggregates metric values using
    the specified estimator and error bar definition, and visualizes the result
    using Matplotlib error bars.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))

    for label in data[hue].unique():
        mse_mean, mse_err = aggregate(
            data[(data[hue] == label)], x, y, estimator=estimator, errorbar=errorbar
        )
        style = styles.get(label, {}) if styles else {}

        plt.errorbar(
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
