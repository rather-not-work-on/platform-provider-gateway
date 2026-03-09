import type { ProviderDriver, ProviderInvocationRequest, ProviderInvocationResult } from "@rather-not-work-on/provider-runtime";

export class ProviderClaudeDriver implements ProviderDriver {
  providerKey(): string {
    return "claude";
  }

  invoke(_request: ProviderInvocationRequest): ProviderInvocationResult {
    return {
      reasonCode: "claude_complete",
    };
  }
}
