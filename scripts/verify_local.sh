#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
bash "${ROOT}/scripts/setup.sh"
source "${ROOT}/.venv/bin/activate"
cellpowertrace run attach_idle_short
cellpowertrace analyze attach_idle_ping --baseline v1
