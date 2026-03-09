import type { ProviderDriverRegistry } from "./provider_driver.js";
import { normalizeProviderOutcome } from "./outcome_policy.js";
import type { ProviderInvocationRequest, ProviderInvocationResult } from "./provider_port.js";
import { resolveProviderKey } from "./routing_policy.js";

export interface ProviderRuntimeDependencies {
  registry?: ProviderDriverRegistry;
  defaultProviderKey?: string;
}

export class ProviderRuntime {
  constructor(private readonly dependencies: ProviderRuntimeDependencies = {}) {}

  invoke(request: ProviderInvocationRequest): ProviderInvocationResult {
    const registeredProviderKeys = this.dependencies.registry?.all().map((driver) => driver.providerKey()) ?? [];
    const providerKey = resolveProviderKey({
      requestedProviderKey: request.providerKey,
      defaultProviderKey: this.dependencies.defaultProviderKey,
      registeredProviderKeys,
    });

    if (!providerKey) {
      return normalizeProviderOutcome({
        reasonCode: "missing_provider",
      });
    }

    const driver = this.dependencies.registry?.find(providerKey);
    if (!driver) {
      return normalizeProviderOutcome({
        reasonCode: "provider_not_registered",
      });
    }

    return normalizeProviderOutcome(driver.invoke(request));
  }
}
