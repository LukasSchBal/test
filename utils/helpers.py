"""Miscellaneous helper utilities."""

import uuid
import hashlib
from typing import Any, List


def generate_id(prefix: str = "") -> str:
    """Return a short unique identifier with an optional prefix."""
    uid = uuid.uuid4().hex[:8]
    return f"{prefix}-{uid}" if prefix else uid


def format_duration(seconds: float) -> str:
    """Convert a duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)}m {int(secs)}s"
    hours, mins = divmod(minutes, 60)
    return f"{int(hours)}h {int(mins)}m"


def flatten(nested: List[Any]) -> List[Any]:
    """Recursively flatten a nested list."""
    result: List[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def compute_checksum(data: str) -> str:
    """Return the SHA-256 hex digest of the given string."""
    return hashlib.sha256(data.encode()).hexdigest()


def chunk_list(lst: List[Any], size: int) -> List[List[Any]]:
    """Split *lst* into consecutive chunks of *size* elements."""
    if size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    return [lst[i : i + size] for i in range(0, len(lst), size)]
