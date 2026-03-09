import type { ProviderDriverRegistry } from "./provider_driver.js";
import type { ProviderInvocationRequest, ProviderInvocationResult } from "./provider_port.js";

export interface ProviderRuntimeDependencies {
  registry?: ProviderDriverRegistry;
}

export class ProviderRuntime {
  constructor(private readonly dependencies: ProviderRuntimeDependencies = {}) {}

  invoke(request: ProviderInvocationRequest): ProviderInvocationResult {
    if (!request.providerKey) {
      return {
        reasonCode: "missing_provider",
      };
    }

    const driver = this.dependencies.registry?.find(request.providerKey);
    if (!driver) {
      return {
        reasonCode: "provider_not_registered",
      };
    }

    const result = driver.invoke(request);
    return {
      reasonCode: result.reasonCode,
    };
  }
}
