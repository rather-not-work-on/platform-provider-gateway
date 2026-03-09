# provider-runtime

Own provider routing and normalized invocation behavior.

- define the runtime-owned driver contract and registry baseline here
- resolve the effective provider through a local routing policy before driver lookup
- normalize inbound invocation request payloads before driver dispatch
- normalize driver result reason codes through a local outcome policy before returning
- choose drivers through the registry instead of hard-coded adapter checks
- planningops policy stays upstream
