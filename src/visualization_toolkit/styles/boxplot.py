"""Styles for the boxplot."""


def boxprops_filled(facecolor: str = "lightgray"):
    """
    Return a dictionary of properties for filled box (style for printing).

    Parameters:
      facecolor (str): The color of the filled box. Default is "white".

    Returns:
       dict: A dictionary containing the properties.
    """
    return {
        "patch_artist": True,
        "flierprops": {
            "markeredgecolor": "black",
            "markeredgewidth": 1.5,
            "markersize": 2,
        },
        "whiskerprops": {"color": "black", "linestyle": "--", "linewidth": 2},
        "capprops": {"color": "black", "linewidth": 2},
        "boxprops": {"facecolor": facecolor, "edgecolor": "black", "linewidth": 2},
        "medianprops": {"color": "black", "linewidth": 2.3},
    }


def boxprops_filled_hatched(facecolor: str = "white", hatch: str = "//"):
    """
    Return a dictionary of properties for hatched box (style for printing).

    Parameters:
      facecolor (str): The color of the filled box. Default is "white".
      hatch (str): The type of hatching pattern. Default is "//".

    Returns:
       dict: A dictionary containing the properties.
    """
    return {
        "patch_artist": True,
        "flierprops": {
            "markeredgecolor": "black",
            "markeredgewidth": 1.5,
            "markersize": 2,
        },
        "whiskerprops": {"color": "black", "linestyle": "--", "linewidth": 2},
        "capprops": {"color": "black", "linewidth": 2},
        "boxprops": {
            "facecolor": facecolor,
            "edgecolor": "black",
            "linewidth": 2,
            "hatch": hatch,
        },
        "medianprops": {"color": "black", "linewidth": 2.3},
    }
