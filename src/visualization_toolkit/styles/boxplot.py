"""Styles for the boxplot."""


def boxprops_filled():
    """
    Return a dictionary of properties for filled box (style for printing).

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
        "boxprops": {"facecolor": "lightgray", "edgecolor": "black", "linewidth": 2},
        "medianprops": {"color": "black", "linewidth": 2.3},
    }


def boxprops_empty():
    """
    Return a dictionary of properties for empty box (style for printing).

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
        "boxprops": {"facecolor": "white", "edgecolor": "black", "linewidth": 2},
        "medianprops": {"color": "black", "linewidth": 2.3},
    }


def boxprops_hatched():
    """
    Return a dictionary of properties for hatched box (style for printing).

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
            "facecolor": "white",
            "edgecolor": "black",
            "linewidth": 2,
            "hatch": "//",
        },
        "medianprops": {"color": "black", "linewidth": 2.3},
    }
