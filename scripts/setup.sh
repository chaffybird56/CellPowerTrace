#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "[setup] Building pm_sim"
make -C "${ROOT}/pm_driver"

if [[ ! -d "${ROOT}/.venv" ]]; then
  python3 -m venv "${ROOT}/.venv"
fi
# shellcheck disable=SC1091
source "${ROOT}/.venv/bin/activate"
pip install -q -U pip
pip install -q -e "${ROOT}/pipeline/python"

echo "[setup] Done. Activate: source ${ROOT}/.venv/bin/activate"
echo "[setup] Try: cellpowertrace run attach_idle_short"
