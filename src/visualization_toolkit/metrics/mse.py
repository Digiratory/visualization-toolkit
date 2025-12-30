"""MSE function"""

import numpy as np

def mse(a: np.ndarray, b: np.ndarray) -> float:
    """Returns the mean squared error between two arrays."""
    return np.mean((a - b) ** 2)
