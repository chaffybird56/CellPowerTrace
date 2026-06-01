from __future__ import annotations

from dataclasses import dataclass

from .kpi import PowerKpi


@dataclass
class RegressionReport:
    baseline_name: str
    candidate_name: str
    connected_delta_pct: float
    score_delta_pct: float
    transition_delta: int
    summary: str


def compare(baseline: PowerKpi, candidate: PowerKpi, baseline_name: str, candidate_name: str) -> RegressionReport:
    b_conn = baseline.connected_fraction or 1e-9
    c_conn = candidate.connected_fraction
    conn_delta = 100.0 * (c_conn - b_conn) / b_conn

    b_score = baseline.weighted_score or 1e-9
    c_score = candidate.weighted_score
    score_delta = 100.0 * (c_score - b_score) / b_score

    t_delta = candidate.transitions - baseline.transitions

    direction = "higher" if conn_delta > 0 else "lower"
    summary = (
        f"Power regression: {conn_delta:+.1f}% time in CONNECTED vs baseline "
        f"({baseline_name} -> {candidate_name}); "
        f"weighted score {score_delta:+.1f}%; transitions {t_delta:+d}."
    )
    return RegressionReport(
        baseline_name=baseline_name,
        candidate_name=candidate_name,
        connected_delta_pct=round(conn_delta, 1),
        score_delta_pct=round(score_delta, 1),
        transition_delta=t_delta,
        summary=summary,
    )
