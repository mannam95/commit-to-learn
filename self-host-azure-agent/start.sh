#!/bin/bash
set -e

if [ -z "${AZP_URL}" ] || [ -z "${AZP_TOKEN}" ]; then
  echo "Missing AZP_URL or AZP_TOKEN"
  exit 1
fi

if [ -n "${AZP_WORK}" ]; then
  mkdir -p "${AZP_WORK}"
fi

cleanup() {
  echo "Cleanup: removing agent..."
  ./config.sh remove --unattended --auth PAT --token "${AZP_TOKEN}" || true
}

trap 'cleanup; exit 0' EXIT
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

./config.sh --unattended \
  --agent "${AZP_AGENT_NAME:-$(hostname)}" \
  --url "${AZP_URL}" \
  --auth PAT \
  --token "${AZP_TOKEN}" \
  --pool "${AZP_POOL:-Default}" \
  --work "${AZP_WORK:-_work}" \
  --replace \
  --acceptTeeEula

./run.sh
