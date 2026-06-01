#!/usr/bin/env bash
# Run a CellPowerTrace scenario: live Docker stack or offline sample logs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCENARIO="${1:-attach_idle_ping}"
USE_DOCKER="${USE_DOCKER:-0}"
RUN_DIR="${ROOT}/runs/$(date +%Y%m%d_%H%M%S)_${SCENARIO}"
mkdir -p "${RUN_DIR}"

echo "[cpt] Scenario: ${SCENARIO}"
echo "[cpt] Run directory: ${RUN_DIR}"

if [[ "${USE_DOCKER}" == "1" ]]; then
  echo "[cpt] Starting Open5GS + UERANSIM (Docker)..."
  docker compose -f "${ROOT}/docker/docker-compose.yml" up -d
  echo "[cpt] Stack up. Capture UE logs from cpt-ueransim container into ${RUN_DIR}/raw_ue.log"
  echo "[cpt] Example: docker logs -f cpt-ueransim 2>&1 | tee ${RUN_DIR}/raw_ue.log"
  exit 0
fi

SAMPLE="${ROOT}/samples/logs/${SCENARIO}_ue.log"
if [[ ! -f "${SAMPLE}" ]]; then
  echo "[cpt] Sample log missing: ${SAMPLE}"
  exit 1
fi

cp "${SAMPLE}" "${RUN_DIR}/raw_ue.log"
echo "[cpt] Using sample log -> ${RUN_DIR}/raw_ue.log"
echo "${RUN_DIR}"
