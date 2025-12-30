"""Statistics Aggregation"""
import numpy as np
import pandas as pd

def aggregate(
    data: pd.DataFrame, x: str, y: str, estimator: str = "mean", errorbar=("p", (5, 95))
):
    """
    Aggregate values of a metric column grouped by unique values of another column.

    For each unique value in column `x`, the function computes a central tendency
    estimate of column `y` (currently only the mean is supported) and asymmetric
    error bars based on percentiles.
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
