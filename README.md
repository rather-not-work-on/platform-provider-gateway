# platform-provider-gateway

Local-first provider gateway baseline for UAP runtime.

## Scope
- LiteLLM-style routing policy skeleton
- primary/fallback invocation flow
- C4 invocation artifact contract smoke checks

## Layout
- `contracts/`: invocation artifact schema
- `config/`: routing policy examples
- `scripts/`: smoke validation scripts and local launcher
- `artifacts/`: smoke execution reports

## Smoke Test
```bash
python3 scripts/litellm_gateway_smoke.py --scenario primary_success
python3 scripts/litellm_gateway_smoke.py --scenario primary_fail_fallback_success
python3 scripts/litellm_gateway_smoke.py --scenario contract_violation
python3 scripts/validate_contract_pin.py
bash scripts/test_provider_guardrails.sh
```

Notes:
- `contract_violation` scenario is expected to fail and verifies guard behavior.
- per-task routing overrides are managed upstream in planningops runtime profiles.

## Local LiteLLM Launcher and Profile Drill
```bash
# local + oracle profile validation drill (non-destructive)
bash scripts/litellm_stack_launcher.sh --mode dry-run

# explicit runtime profile file
bash scripts/litellm_stack_launcher.sh \
  --mode dry-run \
  --runtime-profile-file ../platform-planningops/planningops/config/runtime-profiles.json \
  --profiles local,oracle_cloud
```

Artifacts:
- `artifacts/launcher/<run_id>.json` (profile drill result)
- `artifacts/smoke/*.json` (gateway scenario smoke outputs)

## Local CI Baseline
- workflow: `.github/workflows/provider-local-ci.yml`
- checks:
  - provider smoke (`primary_success`, `primary_fail_fallback_success`)
  - contract pin validation (`scripts/validate_contract_pin.py`)
  - seeded failure guard (`scripts/test_provider_guardrails.sh`)

### Contract Pin Remediation
When contract pin validation fails:
1. Open `config/contract-pin.json`.
2. Ensure:
   - `source_repo == rather-not-work-on/platform-contracts`
   - `consumer_repo == rather-not-work-on/platform-provider-gateway`
   - `contract_bundle_version` format is `YYYY.MM.DD`
   - `pinned_contracts` contains `c4-provider-invocation`
3. Re-run:

```bash
python3 scripts/validate_contract_pin.py
bash scripts/test_provider_guardrails.sh
```
