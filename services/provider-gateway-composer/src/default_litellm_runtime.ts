import { ProviderLocalLlmDriver, type ProviderLocalLlmDriverProfile } from "@rather-not-work-on/provider-local-llm";
import {
  createDefaultProviderRegistry,
  createDefaultProviderRuntime,
  type DefaultProviderRegistryOptions,
} from "./default_provider_registry.js";

export interface LiteLLMRuntimeProfileSource {
  execution_mode: string;
  litellm_base_url: string;
  langfuse_host?: string;
  nanoclaw_endpoint?: string;
}

export interface LiteLLMRuntimeProfileCatalog {
  active_profile?: string;
  profiles: Record<string, LiteLLMRuntimeProfileSource>;
}

export interface LiteLLMLocalRuntimeProfile {
  profileName: string;
  executionMode: string;
  litellmBaseUrl: string;
}

export interface DefaultLiteLLMRuntimeOptions {
  profile: LiteLLMLocalRuntimeProfile;
  registryOptions?: Omit<DefaultProviderRegistryOptions, "localLlmDriver">;
  defaultProviderKey?: string;
}

function buildLocalLlmProfile(profile: LiteLLMLocalRuntimeProfile): ProviderLocalLlmDriverProfile {
  return {
    runtimeProfileName: profile.profileName,
    baseUrl: profile.litellmBaseUrl,
    executionMode: profile.executionMode,
  };
}

export function resolveLiteLLMRuntimeProfile(
  catalog: LiteLLMRuntimeProfileCatalog,
  requestedProfileName = catalog.active_profile,
): LiteLLMLocalRuntimeProfile {
  if (!requestedProfileName) {
    throw new Error("runtime profile name is required");
  }

  const rawProfile = catalog.profiles[requestedProfileName];
  if (!rawProfile) {
    throw new Error(`runtime profile '${requestedProfileName}' is not defined`);
  }

  return {
    profileName: requestedProfileName,
    executionMode: rawProfile.execution_mode,
    litellmBaseUrl: rawProfile.litellm_base_url,
  };
}

export function createDefaultLiteLLMRuntime(options: DefaultLiteLLMRuntimeOptions) {
  const localLlmDriver = new ProviderLocalLlmDriver({
    profile: buildLocalLlmProfile(options.profile),
  });
  const registry = createDefaultProviderRegistry({
    ...options.registryOptions,
    localLlmDriver,
  });

  return createDefaultProviderRuntime({
    defaultProviderKey: options.defaultProviderKey ?? localLlmDriver.providerKey(),
    registry,
  });
}
