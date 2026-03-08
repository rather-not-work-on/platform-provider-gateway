export interface ProviderInvocationRequest {
  providerKey: string;
  prompt: string;
}

export interface ProviderInvocationResult {
  reasonCode: string;
}
