export interface ProviderRoutingPolicyInput {
  requestedProviderKey?: string;
  fallbackProviderKeys?: string[];
  defaultProviderKey?: string;
  registeredProviderKeys: string[];
}

export function resolveProviderKey(input: ProviderRoutingPolicyInput): string | undefined {
  const requestedKeys = [input.requestedProviderKey, ...(input.fallbackProviderKeys ?? [])].filter(
    (value): value is string => Boolean(value),
  );

  for (const requestedKey of requestedKeys) {
    if (input.registeredProviderKeys.includes(requestedKey)) {
      return requestedKey;
    }
  }

  if (input.defaultProviderKey && input.registeredProviderKeys.includes(input.defaultProviderKey)) {
    return input.defaultProviderKey;
  }

  if (input.registeredProviderKeys.length === 1) {
    return input.registeredProviderKeys[0];
  }

  return undefined;
}
