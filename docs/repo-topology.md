# platform-provider-gateway Topology

## Purpose
Fix the long-term repository boundaries before deeper provider runtime implementation begins.

Workspace root descriptors may be added before adapter packages exist. The first scaffold step introduces `services/provider-runtime`; adapter packages follow in a later card.

## Module Map
| Path | Responsibility | Allowed contents | Must not contain |
| --- | --- | --- | --- |
| `contracts/` | Provider-facing artifact contracts and schema-owned interfaces | schema files and contract docs | runtime code, generated reports |
| `config/` | routing policy examples, contract pins, reason taxonomy | static JSON/YAML config and examples | executable logic, runtime evidence |
| `services/` | provider runtime service layer | service packages, package README files, TypeScript source | project policy, generated artifacts |
| `adapters/` | provider-specific adapter packages | adapter packages, package README files, TypeScript source | routing policy, sibling adapter imports |
| `scripts/` | smoke checks, launch helpers, validators | repeatable local tooling and tests | business logic hidden behind ad hoc scripts |
| `docs/runbook/` | operator guidance for smoke evidence and remediation | runbooks and procedures | contracts, runtime outputs |
| `runtime-artifacts/` | gitignored local runtime evidence root | local smoke/launcher outputs plus tracked README | committed runtime reports |

## Extension Rules
1. Add contract/interface changes in `contracts/`.
2. Add routing or reason taxonomy changes in `config/`.
3. Add runtime service code in `services/`.
4. Add provider adapters in `adapters/`.
5. Put repeatable launch/smoke/validation tooling in `scripts/`.
6. Keep operator procedures in `docs/runbook/`.
7. Keep runtime evidence external to Git under `runtime-artifacts/`.

## Ownership Boundary
- `platform-provider-gateway` owns provider invocation smoke/runtime boundary definition.
- Shared contract shape comes from `platform-contracts`.
- Planning/orchestration policy belongs upstream in `platform-planningops`.
