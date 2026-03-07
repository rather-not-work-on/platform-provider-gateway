# Provider Smoke Evidence Runbook

## Goal
Produce schema-valid provider smoke evidence with deterministic reason taxonomy so planningops and cross-repo conformance can consume the result without repo-specific parsing.

## Commands
```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/litellm_gateway_smoke.py --scenario primary_success
python3 scripts/litellm_gateway_smoke.py --scenario primary_fail_fallback_success
python3 scripts/litellm_gateway_smoke.py --scenario contract_violation
python3 scripts/validate_provider_smoke_evidence.py --report runtime-artifacts/smoke/<run_id>-primary_success.json
```

## Reason Taxonomy
- config: `config/provider-reason-taxonomy.json`
- codes:
  - `ok`
  - `fallback_recovered`
  - `contract_violation`
  - `all_providers_failed`

## Evidence Shape
- schema: `contracts/c4-provider-invocation-artifact.schema.json`
- validator: `scripts/validate_provider_smoke_evidence.py`
- report path: `runtime-artifacts/smoke/<run_id>-<scenario>.json`

## Review Checklist
1. `routing_profile` is present and matches the intended test context.
2. `reason_code` exists in taxonomy config.
3. `summary.fallback_used` is true only for fallback scenarios.
4. `attempts[*].validation_status` captures malformed payload rows without making the report itself invalid.
