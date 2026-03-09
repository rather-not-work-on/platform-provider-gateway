import type { ProviderDriver, ProviderInvocationRequest, ProviderInvocationResult } from "@rather-not-work-on/provider-runtime";

export class ProviderLocalLlmDriver implements ProviderDriver {
  providerKey(): string {
    return "local-llm";
  }

  invoke(_request: ProviderInvocationRequest): ProviderInvocationResult {
    return {
      reasonCode: "local_llm_complete",
    };
  }
}
