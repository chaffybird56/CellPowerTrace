from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PowerKpi:
    transitions: int
    time_in_state: dict[str, float]
    weighted_score: float
    connected_fraction: float


def load_trace(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def compute_kpis(trace: list[dict], dwell_ms: float = 500.0) -> PowerKpi:
    if not trace:
        return PowerKpi(0, {}, 0.0, 0.0)

    counts = Counter()
    score_sum = 0.0
    for i, row in enumerate(trace):
        state = row.get("state", "UNKNOWN")
        counts[state] += 1
        score_sum += float(row.get("score_mw", 0))

    transitions = max(0, len(trace) - 1)
    time_in = {s: c * dwell_ms for s, c in counts.items()}
    total_ms = sum(time_in.values()) or 1.0
    connected_ms = time_in.get("CONNECTED", 0.0)
    return PowerKpi(
        transitions=transitions,
        time_in_state=time_in,
        weighted_score=score_sum / max(len(trace), 1),
        connected_fraction=connected_ms / total_ms,
    )


def kpi_to_dict(k: PowerKpi) -> dict:
    return {
        "transitions": k.transitions,
        "time_in_state_ms": k.time_in_state,
        "weighted_score_mw": round(k.weighted_score, 2),
        "connected_fraction": round(k.connected_fraction, 4),
    }
