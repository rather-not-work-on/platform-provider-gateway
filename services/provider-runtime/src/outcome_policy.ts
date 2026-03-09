import type { NormalizedProviderInvocationRequest } from "./request_policy.js";
import type { ProviderInvocationResult } from "./provider_port.js";

const ALLOWED_REASON_CODES = new Set([
  "missing_provider",
  "provider_not_registered",
  "provider_request_invalid",
  "codex_complete",
  "claude_complete",
  "local_llm_complete",
]);

function normalizeReasonCode(reasonCode: string): string {
  if (ALLOWED_REASON_CODES.has(reasonCode)) {
    return reasonCode;
  }

  return "provider_result_unclassified";
}

function inferResultType(reasonCode: string): ProviderInvocationResult["resultType"] {
  if (reasonCode === "missing_provider" || reasonCode === "provider_not_registered") {
    return "failed";
  }

  return "complete";
}

export function normalizeProviderOutcome(
  result: ProviderInvocationResult,
  request?: NormalizedProviderInvocationRequest,
): ProviderInvocationResult {
  const reasonCode = normalizeReasonCode(result.reasonCode);

  return {
    resultType: result.resultType ?? inferResultType(reasonCode),
    reasonCode,
    providerKey: result.providerKey ?? request?.providerKey,
    normalizedPrompt: result.normalizedPrompt ?? request?.prompt,
    outputText: result.outputText,
  };
}
