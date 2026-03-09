import type {
  NormalizedProviderInvocationRequest,
  ProviderDriver,
  ProviderInvocationResult,
} from "@rather-not-work-on/provider-runtime";

export class ProviderClaudeDriver implements ProviderDriver {
  providerKey(): string {
    return "claude";
  }

  invoke(request: NormalizedProviderInvocationRequest): ProviderInvocationResult {
    return {
      resultType: "complete",
      reasonCode: "claude_complete",
      providerKey: request.providerKey,
      normalizedPrompt: request.prompt,
    };
  }
}
