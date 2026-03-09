import type {
  NormalizedProviderInvocationRequest,
  ProviderDriver,
  ProviderInvocationResult,
} from "@rather-not-work-on/provider-runtime";

export class ProviderLocalLlmDriver implements ProviderDriver {
  providerKey(): string {
    return "local-llm";
  }

  invoke(request: NormalizedProviderInvocationRequest): ProviderInvocationResult {
    return {
      resultType: "complete",
      reasonCode: "local_llm_complete",
      providerKey: request.providerKey,
      normalizedPrompt: request.prompt,
    };
  }
}
