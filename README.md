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
