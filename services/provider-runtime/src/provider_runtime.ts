import type { ProviderInvocationRequest, ProviderInvocationResult } from "./provider_port.js";

export class ProviderRuntime {
  invoke(request: ProviderInvocationRequest): ProviderInvocationResult {
    return {
      reasonCode: request.providerKey ? "ok" : "missing_provider",
    };
  }
}
