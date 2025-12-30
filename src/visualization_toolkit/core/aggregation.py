"""Statistics Aggregation"""

import numpy as np
import pandas as pd


def aggregate(
    data: pd.DataFrame, x: str, y: str, estimator: str = "mean", errorbar=("p", (5, 95))
):
    """
    Aggregate a metric grouped by values of another column.

    For each unique value in column `x`, the function computes a central tendency
    estimate of column `y` and corresponding asymmetric error bars.

    Currently supported:
        - estimator: "mean"
        - errorbar: ("p", (low, high)) for percentile-based error bars

    Parameters:
        data (pd.DataFrame):
            Input DataFrame containing at least columns `x` and `y`.

        x (str):
            Name of the column used for grouping.

        y (str):
            Name of the metric column to aggregate.

        estimator (str, default="mean"):
            Aggregation method for the central value.
            Currently only "mean" is supported.

        errorbar (tuple, default=("p", (5, 95))):
            Error bar specification.
            The first element defines the method:
                - "p": percentile-based error bars
            The second element is a tuple of two percentiles (low, high).

    Returns:
        tuple[np.ndarray, np.ndarray]:
            - metric_mean: array of aggregated metric values for each unique `x`
            - metric_err: 2×N array of asymmetric errors
              (lower_errors, upper_errors), suitable for plotting
    """
    x_list = data[x].unique()
    metric_mean_list = []
    metric_err_list = []
    for x_value in x_list:
        part_df = data[data[x] == x_value]
        metric = part_df[y]
        if estimator != "mean":
            raise NotImplementedError(estimator)
        metric_mean = metric.mean()
        metric_mean_list.append(metric_mean)
        if errorbar[0] == "p":
            metric_err = (
                metric_mean - np.percentile(metric, errorbar[1][0]),
                np.percentile(metric, errorbar[1][1]) - metric_mean,
            )
        else:
            raise NotImplementedError(errorbar[0])
        metric_err_list.append(metric_err)
    return np.array(metric_mean_list), np.array(metric_err_list).T
