import type { ProviderInvocationResult } from "./provider_port.js";
import type { NormalizedProviderInvocationRequest } from "./request_policy.js";

export interface ProviderDriver {
  providerKey(): string;
  invoke(request: NormalizedProviderInvocationRequest): ProviderInvocationResult;
}

export interface ProviderDriverRegistry {
  all(): ProviderDriver[];
  find(providerKey: string): ProviderDriver | undefined;
}
