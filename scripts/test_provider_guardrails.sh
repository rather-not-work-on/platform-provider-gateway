#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

RUN_ID="provider-ci-guard"
SMOKE_OUT="$TMP_DIR/smoke"
mkdir -p "$SMOKE_OUT"

python3 "$ROOT_DIR/scripts/litellm_gateway_smoke.py" \
  --scenario primary_success \
  --run-id "$RUN_ID" \
  --output-dir "$SMOKE_OUT"

python3 "$ROOT_DIR/scripts/litellm_gateway_smoke.py" \
  --scenario primary_fail_fallback_success \
  --run-id "$RUN_ID" \
  --output-dir "$SMOKE_OUT"

if python3 "$ROOT_DIR/scripts/litellm_gateway_smoke.py" \
  --scenario contract_violation \
  --run-id "$RUN_ID" \
  --output-dir "$SMOKE_OUT"; then
  echo "[FAIL] contract_violation scenario unexpectedly passed"
  exit 1
fi

python3 "$ROOT_DIR/scripts/validate_contract_pin.py" \
  --output "$TMP_DIR/contract-pin-report.json"

INVALID_PIN="$TMP_DIR/contract-pin.invalid.json"
cat > "$INVALID_PIN" <<'JSON'
{
  "source_repo": "rather-not-work-on/platform-contracts",
  "contract_bundle_version": "2026.02.28",
  "pinned_contracts": [],
  "consumer_repo": "rather-not-work-on/platform-provider-gateway"
}
JSON

if python3 "$ROOT_DIR/scripts/validate_contract_pin.py" \
  --pin "$INVALID_PIN" \
  --output "$TMP_DIR/contract-pin-invalid-report.json"; then
  echo "[FAIL] invalid contract pin unexpectedly passed"
  exit 1
fi

echo "provider guardrails regression passed"
