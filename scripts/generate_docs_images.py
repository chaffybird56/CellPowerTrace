#!/usr/bin/env python3
"""Generate README screenshots (KPI chart + sample CLI transcript)."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "docs" / "images"
IMG.mkdir(parents=True, exist_ok=True)


def chart_from_kpi(kpi_path: Path, out: Path) -> None:
    data = json.loads(kpi_path.read_text(encoding="utf-8"))
    states = list(data["time_in_state_ms"].keys())
    values = [data["time_in_state_ms"][s] / 1000.0 for s in states]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(states, values, color=["#2563eb", "#16a34a", "#ca8a04", "#64748b"][: len(states)])
    ax.set_ylabel("Dwell time (s, model)")
    ax.set_title("Simulated UE power state dwell")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"[docs] {out}")


def cli_transcript_image(out: Path) -> None:
    text = """$ cellpowertrace run attach_idle_ping
[cellpowertrace] trace: runs/.../power_trace.jsonl
{
  "transitions": 7,
  "connected_fraction": 0.375,
  "weighted_score_mw": 220.38
}

$ cellpowertrace analyze attach_idle_ping --baseline v1
Power regression: +21.2% time in CONNECTED vs baseline (v1 -> candidate);
weighted score +17.9%; transitions +3."""
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.axis("off")
    ax.text(0.02, 0.98, text, va="top", family="monospace", fontsize=9)
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    for line in ax.texts:
        line.set_color("#e2e8f0")
    fig.tight_layout()
    fig.savefig(out, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[docs] {out}")


def architecture_image(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis("off")
    boxes = [
        (0.05, 0.55, "Open5GS +\nUERANSIM"),
        (0.28, 0.55, "raw_ue.log\n(NAS/AS)"),
        (0.48, 0.55, "Perl\nnormalize"),
        (0.66, 0.55, "pm_sim\n(C PM)"),
        (0.82, 0.55, "Python\nKPI/regress"),
    ]
    for x, y, label in boxes:
        ax.add_patch(plt.Rectangle((x, y), 0.16, 0.35, fill=True, color="#dbeafe", ec="#1d4ed8"))
        ax.text(x + 0.08, y + 0.17, label, ha="center", va="center", fontsize=8)
    for i in range(len(boxes) - 1):
        ax.annotate("", xy=(boxes[i + 1][0], 0.72), xytext=(boxes[i][0] + 0.16, 0.72),
                    arrowprops=dict(arrowstyle="->", color="#334155"))
    ax.set_title("CellPowerTrace (simulated stack)", fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"[docs] {out}")


def main() -> None:
    kpi = sorted((ROOT / "runs").glob("*_attach_idle_ping/kpi.json"))
    if kpi:
        chart_from_kpi(kpi[-1], IMG / "kpi_chart.png")
    else:
        sample = ROOT / "samples" / "logs" / "attach_idle_ping_ue.log"
        print(f"[docs] skip kpi chart (no run); sample log at {sample}")
    cli_transcript_image(IMG / "cli_output.png")
    architecture_image(IMG / "architecture.png")


if __name__ == "__main__":
    main()
