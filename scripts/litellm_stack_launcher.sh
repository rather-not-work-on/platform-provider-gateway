#!/usr/bin/env bash
set -euo pipefail

MODE="dry-run"
RUNTIME_PROFILE_FILE="../platform-planningops/planningops/config/runtime-profiles.json"
PROFILE_SET="local,oracle_cloud"
RUN_ID="launcher-$(date -u +%Y%m%dT%H%M%SZ)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="$2"
      shift 2
      ;;
    --runtime-profile-file)
      RUNTIME_PROFILE_FILE="$2"
      shift 2
      ;;
    --profiles)
      PROFILE_SET="$2"
      shift 2
      ;;
    --run-id)
      RUN_ID="$2"
      shift 2
      ;;
    *)
      echo "unknown arg: $1"
      exit 2
      ;;
  esac
done

mkdir -p runtime-artifacts/launcher

if [[ "$MODE" == "dry-run" ]]; then
  echo "[launcher] dry-run mode: validating runtime profiles only"
  "$PYTHON_BIN" scripts/litellm_profile_drill.py \
    --runtime-profile-file "$RUNTIME_PROFILE_FILE" \
    --profiles "$PROFILE_SET" \
    --run-id "$RUN_ID"
  exit $?
fi

if [[ "$MODE" == "start" ]]; then
  echo "[launcher] start mode requested"
  if [[ -f "ops/litellm.compose.yaml" ]]; then
    docker compose -f ops/litellm.compose.yaml up -d
  else
    echo "[launcher] compose file not found (ops/litellm.compose.yaml), running profile drill fallback"
  fi
  "$PYTHON_BIN" scripts/litellm_profile_drill.py \
    --runtime-profile-file "$RUNTIME_PROFILE_FILE" \
    --profiles "$PROFILE_SET" \
    --run-id "$RUN_ID"
  exit $?
fi

if [[ "$MODE" == "stop" ]]; then
  echo "[launcher] stop mode requested"
  if [[ -f "ops/litellm.compose.yaml" ]]; then
    docker compose -f ops/litellm.compose.yaml down
  else
    echo "[launcher] compose file not found (ops/litellm.compose.yaml), nothing to stop"
  fi
  exit 0
fi

echo "unsupported mode: $MODE"
exit 2
