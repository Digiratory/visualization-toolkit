"""Signal plotting with mean and confidence interval."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from ..config import get_text


def signal_sigma_plot(
    data: np.ndarray,
    sigma: float = 1.0,
    x: np.ndarray | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    title: str | None = None,
    mean_color: str = "steelblue",
    fill_color: str | None = None,
    fill_alpha: float = 0.3,
    axes_fontsize: int = 22,
    title_fontsize: int = 24,
    ax: matplotlib.axes.Axes | None = None,
    **kwargs,
) -> matplotlib.axes.Axes:
    """
    Plot the mean signal with a confidence interval of ±sigma standard deviations.

    Parameters:
        data (numpy.ndarray): Input array of shape (i, n), where i is the number
            of measurements at each time point and n is the signal length.

        sigma (float, default=1.0): Number of standard deviations for the
            confidence interval band (fill_between).

        x (numpy.ndarray or None, default=None): Optional 1-D array of length n
            used as the x-axis. If None, integer indices 0..n-1 are used.

        x_label (str or None, default=None): Label for the x-axis.
            If None: localized default;
            If "": no label.

        y_label (str or None, default=None): Label for the y-axis.
           If None: localized default;
           If "": no label.

        title (str or None, default=None): Plot title.
            If "": no title.

        mean_color (str, default="steelblue"): Color of the mean line.

        fill_color (str or None, default=None): Color of the confidence band.
            If None, the same color as mean_color is used.

        fill_alpha (float, default=0.3): Transparency of the confidence band.

        axes_fontsize (int, default=22): Font size for axis labels
            and ticks labels are set to axes_fontsize - 4.

        title_fontsize (int, default=24): Font size for the plot title.

        ax (matplotlib.axes.Axes or None, default=None): Existing axes to draw on.
            If None, a new figure and axes are created.

        **kwargs: Additional keyword arguments forwarded to ``ax.plot`` for the
            mean line.

    Returns:
        matplotlib.axes.Axes: The axes object containing the plot.
    """
    data = np.asarray(data)
    if data.ndim != 2:
        raise ValueError(f"data must be 2-D (i x n), got shape {data.shape}")

    mean = data.mean(axis=0)
    std = data.std(axis=0)

    if x is None:
        x = np.arange(data.shape[1])

    if x_label is None:
        x_label = get_text("x_label_sample")
    if y_label is None:
        y_label = get_text("y_label_amplitude")
    if fill_color is None:
        fill_color = mean_color

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))

    ax.plot(x, mean, color=mean_color, **kwargs)
    ax.tick_params(axis="both", labelsize=axes_fontsize - 4)
    ax.fill_between(
        x,
        mean - sigma * std,
        mean + sigma * std,
        color=fill_color,
        alpha=fill_alpha,
    )

    if x_label != "":
        ax.set_xlabel(x_label, fontsize=axes_fontsize)
    if y_label != "":
        ax.set_ylabel(y_label, fontsize=axes_fontsize)
    if title != "":
        ax.set_title(title, fontsize=title_fontsize)
    ax.grid(True)
    return ax
