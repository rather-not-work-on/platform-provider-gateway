import type { ProviderInvocationRequest, ProviderInvocationResult } from "./provider_port.js";

export interface ProviderDriver {
  providerKey(): string;
  invoke(request: ProviderInvocationRequest): ProviderInvocationResult;
}

export interface ProviderDriverRegistry {
  all(): ProviderDriver[];
  find(providerKey: string): ProviderDriver | undefined;
}
