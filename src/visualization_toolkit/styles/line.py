"""Styles for line plots."""

line_markers = [
    "o",  # circle
    "s",  # square
    "p",  # pentagon
    "v",  # triangle_down
    "<",  # triangle_left
    ">",  # triangle_right
    "^",  # triangle_up
    "*",  # star
    "h",  # hexagon
    "8",  # octagon
]


def _base_linestyle(
    marker: str,
    linestyle: str = "-",
    markerfacecolor: str = "none",
    markeredgecolor: str = "black",
    markersize: int = 8,
    linewidth: float = 1.5,
    color: str = "black",
):
    """
    Base style factory for line plots.

    Args:
        marker (str): Marker style for data points (e.g., "o", "s", "^").
        linestyle (str): Line style for the plot (e.g., "-", "--").
        markerfacecolor (str): Color used to fill the marker face. Use "none" for hollow markers.
        markeredgecolor (str): Color of the marker edge.
        markersize (int): Size of the markers.
        linewidth (float): Width of the line.
        color (str): Color of the line and, by default, marker edge.

    Returns:
        dict: Keyword arguments configuring marker and line appearance,
        suitable for passing to ``matplotlib.pyplot.plot`` or similar APIs.
    """
    return {
        "marker": marker,
        "linestyle": linestyle,
        "markerfacecolor": markerfacecolor,
        "markeredgecolor": markeredgecolor,
        "markersize": markersize,
        "linewidth": linewidth,
        "color": color,
    }


def line_empty_marker(marker="o", color="black", linestyle="-"):
    """
    Line style with empty markers and a solid line.

    Args:
        marker (str): Marker style for the points (e.g., "o", "s", "^").
        color (str | None): Color for the line and marker edges. If ``None``,
            the plotting library's default color is used.
        linestyle (str): Line style string (e.g., "-", "--", ":").
    Returns:
        dict: Keyword arguments configuring marker and line appearance,
        suitable for passing to ``matplotlib.pyplot.plot`` or similar APIs.
    """
    return _base_linestyle(
        marker=marker,
        linestyle=linestyle,
        markerfacecolor="none",
        markeredgecolor=color,
        color=color,
    )


def line_filled_marker(marker="o", color="black", facecolor=None, linestyle="-"):
    """
    Line with filled markers.

    Args:
        marker (str, optional): Marker style for the data points (e.g. "o", "s").
        color (str, optional): Color for the line and marker edges.
        facecolor (str, optional): Fill color for the markers. If None, defaults to ``color``.
        linestyle (str, optional): Line style for the plot (e.g. "-", "--").
    Returns:
        dict: Keyword arguments configuring marker and line appearance,
        suitable for passing to ``matplotlib.pyplot.plot`` or similar APIs.
    """
    if facecolor is None:
        facecolor = color
    return _base_linestyle(
        marker=marker,
        linestyle=linestyle,
        markerfacecolor=facecolor,
        markeredgecolor=color,
        color=color,
    )
