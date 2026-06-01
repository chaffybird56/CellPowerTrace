# Flows

## Offline demo (default)

```bash
bash scripts/setup.sh && source .venv/bin/activate
./scripts/run_scenario.sh attach_idle_ping
RUN=$(ls -1d runs/*_attach_idle_ping | tail -1)
perl pipeline/perl/normalize_logs.pl --in "$RUN/raw_ue.log" --out "$RUN/events.jsonl"
./pm_driver/pm_sim "$RUN/events.jsonl" "$RUN/power_trace.jsonl"
cellpowertrace analyze attach_idle_ping --baseline v1
```

## Docker (Open5GS + UERANSIM)

```bash
docker compose -f docker/docker-compose.yml up -d
USE_DOCKER=1 ./scripts/run_scenario.sh attach_idle_ping
```

Exec into `cpt-ueransim` per [Gradiant UERANSIM image](https://hub.docker.com/r/gradiant/ueransim) docs to start gNB/UE and stream logs into `runs/<id>/raw_ue.log`.

## CI

GitHub Actions builds `pm_sim`, runs `attach_idle_short`, and regression smoke on `attach_idle_ping` sample logs—no Docker in CI.
