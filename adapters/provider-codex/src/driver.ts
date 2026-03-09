import type {
  NormalizedProviderInvocationRequest,
  ProviderDriver,
  ProviderInvocationResult,
} from "@rather-not-work-on/provider-runtime";

export class ProviderCodexDriver implements ProviderDriver {
  providerKey(): string {
    return "codex";
  }

  invoke(request: NormalizedProviderInvocationRequest): ProviderInvocationResult {
    return {
      resultType: "complete",
      reasonCode: "codex_complete",
      providerKey: request.providerKey,
      normalizedPrompt: request.prompt,
    };
  }
}
