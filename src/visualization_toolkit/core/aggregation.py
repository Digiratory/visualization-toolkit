"""Statistics Aggregation"""

import numpy as np
import pandas as pd


def aggregate(
    data: pd.DataFrame,
    x: str,
    y: str,
    estimator: str = "median",
    errorbar_type="p",
    errorbar_data=(5, 95),
):
    """
    Aggregate a metric grouped by values of another column.

    For each unique value in column `x`, the function computes a central tendency
    estimate of column `y` and corresponding asymmetric error bars.

    Currently supported:
        - estimator: "mean" | "median"
        - errorbar_type: "p", for percentile-based error bars
        - errorbar_data: (0, 95), for percentile-based error bars

    Parameters:
        data (pd.DataFrame):
            Input DataFrame containing at least columns `x` and `y`.

        x (str):
            Name of the column used for grouping.

        y (str):
            Name of the metric column to aggregate.

        estimator (str, default="median"):
            Aggregation method for the central value.
            Currently "mean" ot "median" are supported.

        errorbar_type (str, default="p"):
            Error bar specification.
                - "p": percentile-based error bars
        errorbar_data (tuple, default=(0, 95)):
            Error bar specification.
            The tuple of data. Default is two percentiles (low, high) for percentile-based error bars.

    Returns:
        tuple[np.ndarray, np.ndarray]:
            - metric_list: array of aggregated metric values for each unique `x`
            - metric_err: 2×N array of asymmetric errors
              (lower_errors, upper_errors), suitable for plotting
    """
    x_list = data[x].unique()
    metric_list = []
    metric_err_list = []
    for x_value in x_list:
        part_df = data[data[x] == x_value]
        metric = part_df[y]
        if estimator == "mean":
            center = metric.mean()
        elif estimator == "median":
            center = metric.median()
        else:
            raise NotImplementedError(estimator)
        metric_list.append(center)
        if errorbar_type == "p":
            p_low, p_high = np.percentile(metric, errorbar_data)
            metric_err = (
                center - p_low,
                p_high - center,
            )
        else:
            raise NotImplementedError(errorbar_type)
        metric_err_list.append(metric_err)
    return np.array(metric_list), np.array(metric_err_list).T
