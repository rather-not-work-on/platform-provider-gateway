# platform-provider-gateway

Local-first provider gateway baseline for UAP runtime.

## Scope
- LiteLLM-style routing policy skeleton
- primary/fallback invocation flow
- C4 invocation artifact contract smoke checks
- repo-owned smoke evidence schema and reason taxonomy

## Layout
- `contracts/`: invocation artifact schema
- `config/`: routing policy examples
- `scripts/`: smoke validation scripts and local launcher
- `docs/runbook/`: operational smoke/runbook guidance
- `runtime-artifacts/`: default local smoke execution reports (gitignored)
- `docs/`: repository topology and extension guidance

Topology guide:
- `docs/repo-topology.md`
- `contracts/README.md`
- `config/README.md`
- `scripts/README.md`
- `docs/runbook/README.md`
- `runtime-artifacts/README.md`

## Workspace Bootstrap
- `package.json`
- `pnpm-workspace.yaml`
- `tsconfig.base.json`
- `services/provider-runtime/`

The workspace bootstrap is intentionally thin in this step.

- current Python scripts remain smoke and launcher tooling
- local runtime outputs stay under `runtime-artifacts/`
- provider adapters now implement the runtime-owned driver contract
- provider-runtime now owns the registry baseline that selects registered drivers
- provider-runtime also owns the routing policy baseline that resolves the effective provider key
- provider-runtime also owns the outcome policy baseline that normalizes public reason codes

Current scaffolded runtime packages:
- `services/provider-runtime`
- `adapters/provider-codex`
- `adapters/provider-claude`
- `adapters/provider-local-llm`

## Smoke Test
```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/litellm_gateway_smoke.py --scenario primary_success
python3 scripts/litellm_gateway_smoke.py --scenario primary_fail_fallback_success
python3 scripts/litellm_gateway_smoke.py --scenario contract_violation
python3 scripts/validate_provider_smoke_evidence.py --report runtime-artifacts/smoke/<run_id>-primary_success.json
python3 scripts/validate_reason_taxonomy_map.py
python3 scripts/validate_contract_pin.py
bash scripts/test_provider_guardrails.sh
```

Notes:
- `contract_violation` scenario is expected to fail and verifies guard behavior.
- per-task routing overrides are managed upstream in planningops runtime profiles.
- schema validation prefers `jsonschema` when installed and falls back to `scripts/jsonschema_compat.py` in offline environments.

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
- `runtime-artifacts/launcher/<run_id>.json` (profile drill result)
- `runtime-artifacts/smoke/*.json` (gateway scenario smoke outputs)
- runbook: `docs/runbook/provider-smoke-evidence-runbook.md`

## Local CI Baseline
- workflow: `.github/workflows/provider-local-ci.yml`
- checks:
  - provider smoke (`primary_success`, `primary_fail_fallback_success`)
  - smoke evidence schema validation (`scripts/validate_provider_smoke_evidence.py`)
  - provider reason taxonomy map validation (`scripts/validate_reason_taxonomy_map.py`)
  - contract pin validation (`scripts/validate_contract_pin.py`)
  - seeded failure guard (`scripts/test_provider_guardrails.sh`)
  - topology/module README regression (`scripts/test_module_readmes.sh`)

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

## PR Hygiene
- template: `.github/pull_request_template.md`
- review gate: `.github/workflows/pr-review-gate.yml`
- external repo PRs must include a repo-qualified planningops issue ref
- example: `Closes rather-not-work-on/platform-planningops#208`

Generated local runtime outputs stay under `runtime-artifacts/` and remain gitignored except for the tracked module README.
