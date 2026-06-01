# CellPowerTrace

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](docker/)

Cellular power regression analyzer for **simulated** 5G UE stacks. Runs attach → idle → data → idle scenarios against Open5GS + UERANSIM (or bundled sample logs), maps NAS/AS events through a userspace power-state simulator, and reports KPIs and baseline deltas.

**Resume-accurate framing:** analyzed open-source / simulated cellular stack logs; built a simulated modem PM interface and Perl/Python log pipeline—not production modem drivers or handset QXDM captures.

## Status

| Section | Contents |
|---------|----------|
| ✅ Scaffold | Layout, architecture doc, license |
| 🔲 Stack | Docker Compose, scenario runner |
| 🔲 PM driver | C state machine + power trace writer |
| 🔲 Perl pipeline | Log normalization |
| 🔲 Python CLI | KPIs, regression, `cellpowertrace` command |
| 🔲 CI | GitHub Actions on sample scenarios |
| 🔲 Docs | Screenshots, full quickstart |

## Planned layout

```
docker/                 # Open5GS + UERANSIM Compose
scenarios/              # attach_idle_ping.yaml, etc.
pm_driver/              # Simulated PM (C)
pipeline/perl/          # Log normalization
pipeline/python/        # KPI + regression CLI
samples/logs/           # Offline sample UE logs
scripts/                # run_scenario.sh, setup
docs/images/            # CLI and architecture screenshots
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for data flow and honest scope notes.

## License

MIT — see [LICENSE](LICENSE).
