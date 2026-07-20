"""Small standard-library analysis helpers used by the demo.

The information-gain value is kept as a legacy exploratory metric from the
original bachelor-thesis prototype. It is not a claim of causal importance or
production-grade fingerprint quality.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence

from db import FINGERPRINT_COLUMNS


def entropy(values: Iterable[str]) -> float:
    """Return Shannon entropy in bits for a sequence of categorical values."""
    cleaned = ["" if value is None else str(value) for value in values]
    if not cleaned:
        return 0.0

    counts = Counter(cleaned)
    total = len(cleaned)
    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
        if count
    )


def information_gain(members: Sequence[str], split: Sequence[str]) -> float:
    """Return H(members) - H(members | split) for categorical values."""
    if not members or len(members) != len(split):
        return 0.0

    grouped: dict[str, list[str]] = defaultdict(list)
    for member, split_value in zip(members, split, strict=True):
        grouped[str(split_value)].append(str(member))

    total = len(members)
    conditional_entropy = sum(
        (len(group) / total) * entropy(group) for group in grouped.values()
    )
    return max(0.0, entropy(members) - conditional_entropy)


def analyse(rows: Sequence[Mapping[str, str]]) -> dict[str, object]:
    """Calculate entropy and the legacy pairwise information-gain heuristic."""
    values_by_column = {
        column: [str(row.get(column, "")) for row in rows]
        for column in FINGERPRINT_COLUMNS
    }
    entropy_by_column = {
        column: entropy(values) for column, values in values_by_column.items()
    }

    ordered_columns = sorted(
        FINGERPRINT_COLUMNS,
        key=lambda column: entropy_by_column[column],
        reverse=True,
    )

    gain_by_column = {column: 0.0 for column in FINGERPRINT_COLUMNS}
    if len(rows) >= 2 and ordered_columns:
        reference = ordered_columns[0]
        secondary = ordered_columns[1] if len(ordered_columns) > 1 else reference
        for column in ordered_columns:
            split_column = secondary if column == reference else reference
            gain_by_column[column] = information_gain(
                values_by_column[column], values_by_column[split_column]
            )

    return {
        "sample_count": len(rows),
        "order": ordered_columns,
        "entropy": {
            column: round(entropy_by_column[column], 6)
            for column in ordered_columns
        },
        "information_gain": {
            column: round(gain_by_column[column], 6)
            for column in ordered_columns
        },
    }
