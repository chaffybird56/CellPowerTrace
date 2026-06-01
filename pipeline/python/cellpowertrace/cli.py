from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .kpi import compute_kpis, kpi_to_dict, load_trace
from .regression import compare


def _root() -> Path:
    return Path(__file__).resolve().parents[3]


def _scenario_runs(root: Path, scenario: str) -> list[Path]:
    return sorted(
        p for p in (root / "runs").glob(f"*_{scenario}")
        if p.is_dir() and p.name[0].isdigit()
    )


def _run_pipeline(scenario: str, run_dir: Path) -> Path:
    root = _root()
    raw = run_dir / "raw_ue.log"
    if not raw.exists():
        raise SystemExit(f"Missing raw log: {raw}")

    events = run_dir / "events.jsonl"
    trace = run_dir / "power_trace.jsonl"

    subprocess.run(
        ["perl", str(root / "pipeline" / "perl" / "normalize_logs.pl"),
         "--in", str(raw), "--out", str(events)],
        check=True,
        cwd=root,
    )

    pm = root / "pm_driver" / "pm_sim"
    if not pm.exists():
        subprocess.run(["make", "-C", str(root / "pm_driver")], check=True)

    subprocess.run([str(pm), str(events), str(trace)], check=True, cwd=root)
    return trace


def cmd_run(args: argparse.Namespace) -> int:
    root = _root()
    subprocess.run(
        [str(root / "scripts" / "run_scenario.sh"), args.scenario],
        check=True,
        cwd=root,
    )
    runs = _scenario_runs(root, args.scenario)
    if not runs:
        raise SystemExit(f"No run directory for scenario {args.scenario}")
    trace = _run_pipeline(args.scenario, runs[-1])
    kpi = compute_kpis(load_trace(trace))
    out = runs[-1] / "kpi.json"
    out.write_text(json.dumps(kpi_to_dict(kpi), indent=2) + "\n", encoding="utf-8")
    print(f"[cellpowertrace] trace: {trace}")
    print(f"[cellpowertrace] kpi:   {out}")
    print(json.dumps(kpi_to_dict(kpi), indent=2))
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    root = _root()
    baseline_dir = _scenario_runs(root, args.scenario)
    if not baseline_dir:
        raise SystemExit(f"No runs for scenario {args.scenario}; run without --baseline first")

    base_trace = _run_pipeline(args.scenario, baseline_dir[-1])
    base_kpi = compute_kpis(load_trace(base_trace))

    cand_name = args.candidate or f"{args.scenario}_regress"
    sample = root / "samples" / "logs" / f"{cand_name}_ue.log"
    if not sample.exists():
        sample = root / "samples" / "logs" / f"{args.scenario}_regress_ue.log"
    if not sample.exists():
        raise SystemExit(f"Candidate log not found for {cand_name}")

    cand_dir = root / "runs" / f"regress_{args.scenario}"
    cand_dir.mkdir(parents=True, exist_ok=True)
    (cand_dir / "raw_ue.log").write_text(sample.read_text(encoding="utf-8"), encoding="utf-8")
    cand_trace = _run_pipeline(args.scenario, cand_dir)
    cand_kpi = compute_kpis(load_trace(cand_trace))

    label_b = args.baseline or "baseline"
    label_c = args.candidate or "candidate"
    report = compare(base_kpi, cand_kpi, label_b, label_c)
    print(report.summary)
    report_path = cand_dir / "regression.txt"
    report_path.write_text(report.summary + "\n", encoding="utf-8")
    print(f"[cellpowertrace] report: {report_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cellpowertrace")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run scenario and compute KPIs")
    p_run.add_argument("scenario", nargs="?", default="attach_idle_ping")
    p_run.set_defaults(func=cmd_run)

    p_an = sub.add_parser("analyze", help="Compare run vs baseline")
    p_an.add_argument("scenario", nargs="?", default="attach_idle_ping")
    p_an.add_argument("--baseline", default="v1")
    p_an.add_argument("--candidate", default=None)
    p_an.set_defaults(func=cmd_analyze)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
