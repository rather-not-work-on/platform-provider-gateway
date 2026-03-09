import type { ProviderDriverRegistry } from "./provider_driver.js";
import { normalizeProviderOutcome } from "./outcome_policy.js";
import type { ProviderInvocationRequest, ProviderInvocationResult } from "./provider_port.js";
import { normalizeProviderRequest } from "./request_policy.js";
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
      fallbackProviderKeys: request.fallbackProviderKeys,
      defaultProviderKey: this.dependencies.defaultProviderKey,
      registeredProviderKeys,
    });

    if (!providerKey) {
      return normalizeProviderOutcome({
        resultType: "failed",
        reasonCode: "missing_provider",
      });
    }

    const normalizedRequest = normalizeProviderRequest(request, providerKey);

    const driver = this.dependencies.registry?.find(providerKey);
    if (!driver) {
      return normalizeProviderOutcome({
        resultType: "failed",
        reasonCode: "provider_not_registered",
      }, normalizedRequest);
    }

    return normalizeProviderOutcome(driver.invoke(normalizedRequest), normalizedRequest);
  }
}
