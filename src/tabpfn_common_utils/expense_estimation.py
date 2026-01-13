from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager

from tabpfn_common_utils.telemetry import telemetry_context


@contextmanager
def estimate_expenses(
    model_name: str,
    num_samples: int,
    num_features: int,
    num_classes: int = 2,
    device: str = "cpu",
) -> Iterator[None]:
    """Estimate the expenses of a function call."""
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        telemetry_context.record_expense(
            model_name=model_name,
            duration=duration,
            num_samples=num_samples,
            num_features=num_features,
            num_classes=num_classes,
            device=device,
        )
