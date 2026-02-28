# platform-provider-gateway

Local-first provider gateway baseline for UAP runtime.

## Scope
- LiteLLM-style routing policy skeleton
- primary/fallback invocation flow
- C4 invocation artifact contract smoke checks

## Layout
- `contracts/`: invocation artifact schema
- `config/`: routing policy examples
- `scripts/`: smoke validation scripts
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
