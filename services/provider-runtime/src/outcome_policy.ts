import type { ProviderInvocationResult } from "./provider_port.js";

const ALLOWED_REASON_CODES = new Set([
  "missing_provider",
  "provider_not_registered",
  "codex_complete",
  "claude_complete",
  "local_llm_complete",
]);

export function normalizeProviderOutcome(result: ProviderInvocationResult): ProviderInvocationResult {
  if (ALLOWED_REASON_CODES.has(result.reasonCode)) {
    return result;
  }

  return {
    reasonCode: "provider_result_unclassified",
  };
}
