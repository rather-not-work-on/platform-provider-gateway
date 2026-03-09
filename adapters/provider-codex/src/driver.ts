import type { ProviderDriver, ProviderInvocationRequest, ProviderInvocationResult } from "@rather-not-work-on/provider-runtime";

export class ProviderCodexDriver implements ProviderDriver {
  providerKey(): string {
    return "codex";
  }

  invoke(_request: ProviderInvocationRequest): ProviderInvocationResult {
    return {
      reasonCode: "codex_complete",
    };
  }
}
