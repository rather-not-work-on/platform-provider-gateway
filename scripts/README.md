# scripts

## Responsibility
Host repeatable local smoke, validation, and launcher tooling.

## Contents
- gateway smoke scenarios
- launcher-backed live smoke wrapper
- evidence validators
- reason taxonomy map validator
- contract pin validation
- stack launcher helpers

## Rules
- scripts should emit runtime output into `runtime-artifacts/` or `/tmp`, not Git-tracked paths
- repository topology drift must be caught by `test_module_readmes.sh`
