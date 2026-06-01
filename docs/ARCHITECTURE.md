# CellPowerTrace architecture

## Scope (software-only, honest labeling)

This project analyzes **simulated** cellular UE stacks (Open5GS + UERANSIM in Docker, or curated sample logs). It does **not** use Qualcomm production modem firmware or QXDM captures from shipped handsets.

| Layer | Role |
|-------|------|
| **Stack** | Docker Compose runs 5G SA core + UE; scenarios drive attach → idle → traffic → idle → detach |
| **PM simulator** | C userspace module maps NAS/AS events to power states (IDLE, CONNECTED, DRX, DEEP_SLEEP) |
| **Perl pipeline** | Normalizes raw stack text into structured records (telecom log preprocessing) |
| **Python analytics** | KPIs, baseline comparison, regression scoring, CLI |
| **Artifacts** | Unified power trace log + JSON/terminal report |

## Data flow

```
scenario.yaml
    → run_scenario.sh (Docker / sample logs)
    → raw_ue.log (NAS / RRC lines)
    → normalize_logs.pl
    → events.jsonl
    → pm_sim (state transitions + power trace)
    → power_trace.jsonl
    → cellpowertrace analyze (KPI + regression vs baseline)
    → report (CLI + optional plot)
```

## Power states (simulated PM)

| State | Typical trigger (parsed event) |
|-------|--------------------------------|
| IDLE | Default / detach complete |
| CONNECTED | Registration accept, RRC connected |
| DRX | Configured DRX / idle with paging |
| DEEP_SLEEP | Extended idle profile in scenario |

Estimated power score is a **unitless model** (mW weights per state × dwell time), for regression comparison only—not calibrated to silicon.
