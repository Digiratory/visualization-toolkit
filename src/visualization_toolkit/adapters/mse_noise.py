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
    Returns tidy DataFrame with columns:
    snr, mse, label, run
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
                rows.append({
                    "snr": snr,
                    "mse": mse(
                        original_signals[idx],
                        signal[idx],
                    ),
                    "label": label,
                    "run": run,
                })

    return pd.DataFrame(rows)
