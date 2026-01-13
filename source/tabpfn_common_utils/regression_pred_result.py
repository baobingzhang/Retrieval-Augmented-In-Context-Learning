from __future__ import annotations

import dataclasses
from typing import Optional

import numpy as np


@dataclasses.dataclass
class RegressionPredictionResult:
    """Container for regression predictions."""

    predictions: np.ndarray
    """The predictions of the model."""

    quantiles: Optional[np.ndarray] = None
    """The quantiles of the predictions."""

    def to_numpy(self) -> np.ndarray:
        """Convert the result to a numpy array."""
        return self.predictions
