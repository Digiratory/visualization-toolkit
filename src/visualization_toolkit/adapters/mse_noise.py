"""MSE Noise Experiment"""

import numpy as np
import pandas as pd

from ..metrics.mse import mse


def mse_noise_experiment(
    original_signals: np.ndarray,
    signals: dict[str, np.ndarray],
    noise_levels,
) -> pd.DataFrame:
    """
    Computes MSE between clean and noisy/reconstructed signals for different
    noise levels and returns the results in a tidy DataFrame.

    The function assumes that signals are ordered such that for each noise
    level there are `n_samples` consecutive signal realizations.

    Returns a DataFrame with the following columns:
        - snr: signal-to-noise ratio in dB (20 * log10(noise_level))
        - mse: mean squared error between clean and corresponding signal
        - label: key from the `signals` dictionary identifying the method/signal
        - run: index of the run within the same noise level

    Parameters:
        original_signals (np.ndarray):
            Array of clean reference signals with shape
            (n_levels * n_samples, ...).

        signals (dict[str, np.ndarray]):
            Dictionary mapping signal labels to arrays of signals
            (e.g. noisy or reconstructed), each having the same shape
            and ordering as `original_signals`.

        noise_levels (array-like):
            Sequence of noise level ratios corresponding to signal blocks.

    Returns:
        pd.DataFrame:
            DataFrame containing MSE statistics for each signal,
            noise level, and run.
    """
    noise_levels = np.asarray(noise_levels)
    n_ratios = len(noise_levels)
    n_samples = len(original_signals) // n_ratios
    rows = []
    for label, signal in signals.items():
        for i, ratio in enumerate(noise_levels):
            for run in range(n_samples):
                idx = i * n_samples + run
                snr = 20 * np.log10(ratio)
                rows.append(
                    {
                        "snr": snr,
                        "mse": mse(
                            original_signals[idx],
                            signal[idx],
                        ),
                        "label": label,
                        "run": run,
                    }
                )

    return pd.DataFrame(rows)
