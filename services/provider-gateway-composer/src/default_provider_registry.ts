import { ProviderClaudeDriver } from "@rather-not-work-on/provider-claude";
import { ProviderCodexDriver } from "@rather-not-work-on/provider-codex";
import { ProviderLocalLlmDriver } from "@rather-not-work-on/provider-local-llm";
import {
  ProviderRuntime,
  StaticProviderDriverRegistry,
  type ProviderDriver,
  type ProviderDriverRegistry,
  type ProviderRuntimeDependencies,
} from "@rather-not-work-on/provider-runtime";

export interface DefaultProviderRegistryOptions {
  codexDriver?: ProviderDriver;
  claudeDriver?: ProviderDriver;
  localLlmDriver?: ProviderDriver;
}

export function buildDefaultProviderDrivers(options: DefaultProviderRegistryOptions = {}): ProviderDriver[] {
  return [
    options.codexDriver ?? new ProviderCodexDriver(),
    options.claudeDriver ?? new ProviderClaudeDriver(),
    options.localLlmDriver ?? new ProviderLocalLlmDriver(),
  ];
}

export function createDefaultProviderRegistry(options: DefaultProviderRegistryOptions = {}): ProviderDriverRegistry {
  return new StaticProviderDriverRegistry(buildDefaultProviderDrivers(options));
}

export function createDefaultProviderRuntime(
  dependencies: ProviderRuntimeDependencies & { registry?: ProviderDriverRegistry } = {},
): ProviderRuntime {
  return new ProviderRuntime({
    ...dependencies,
    registry: dependencies.registry ?? createDefaultProviderRegistry(),
  });
}
