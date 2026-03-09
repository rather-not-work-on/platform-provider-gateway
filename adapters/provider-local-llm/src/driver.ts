import type {
  NormalizedProviderInvocationRequest,
  ProviderDriver,
  ProviderInvocationResult,
} from "@rather-not-work-on/provider-runtime";

export interface ProviderLocalLlmDriverProfile {
  runtimeProfileName: string;
  baseUrl: string;
  executionMode?: string;
}

export interface ProviderLocalLlmDriverOptions {
  profile?: ProviderLocalLlmDriverProfile;
}

export class ProviderLocalLlmDriver implements ProviderDriver {
  constructor(private readonly options: ProviderLocalLlmDriverOptions = {}) {}

  providerKey(): string {
    return "local-llm";
  }

  invoke(request: NormalizedProviderInvocationRequest): ProviderInvocationResult {
    return {
      resultType: "complete",
      reasonCode: this.options.profile ? "local_llm_profiled" : "local_llm_complete",
      providerKey: request.providerKey,
      normalizedPrompt: request.prompt,
    };
  }
}
