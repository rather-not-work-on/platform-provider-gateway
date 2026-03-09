export interface ProviderRoutingPolicyInput {
  requestedProviderKey?: string;
  defaultProviderKey?: string;
  registeredProviderKeys: string[];
}

export function resolveProviderKey(input: ProviderRoutingPolicyInput): string | undefined {
  if (input.requestedProviderKey) {
    return input.requestedProviderKey;
  }

  if (input.defaultProviderKey) {
    return input.defaultProviderKey;
  }

  if (input.registeredProviderKeys.length === 1) {
    return input.registeredProviderKeys[0];
  }

  return undefined;
}
