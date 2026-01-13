from __future__ import annotations

import hashlib
import json
from typing import Any


def calculate_fingerprint(data: Any) -> str:
    """Calculate a fingerprint for the given data."""
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(str(data).encode()).hexdigest()
