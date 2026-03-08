# platform-provider-gateway Topology

## Purpose
Fix the long-term repository boundaries before deeper provider runtime implementation begins.

## Module Map
| Path | Responsibility | Allowed contents | Must not contain |
| --- | --- | --- | --- |
| `contracts/` | Provider-facing artifact contracts and schema-owned interfaces | schema files and contract docs | runtime code, generated reports |
| `config/` | routing policy examples, contract pins, reason taxonomy | static JSON/YAML config and examples | executable logic, runtime evidence |
| `scripts/` | smoke checks, launch helpers, validators | repeatable local tooling and tests | business logic hidden behind ad hoc scripts |
| `docs/runbook/` | operator guidance for smoke evidence and remediation | runbooks and procedures | contracts, runtime outputs |
| `runtime-artifacts/` | gitignored local runtime evidence root | local smoke/launcher outputs plus tracked README | committed runtime reports |

## Extension Rules
1. Add contract/interface changes in `contracts/`.
2. Add routing or reason taxonomy changes in `config/`.
3. Put repeatable launch/smoke/validation tooling in `scripts/`.
4. Keep operator procedures in `docs/runbook/`.
5. Keep runtime evidence external to Git under `runtime-artifacts/`.

## Ownership Boundary
- `platform-provider-gateway` owns provider invocation smoke/runtime boundary definition.
- Shared contract shape comes from `platform-contracts`.
- Planning/orchestration policy belongs upstream in `platform-planningops`.
