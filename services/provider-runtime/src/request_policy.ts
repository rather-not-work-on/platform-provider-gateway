import type { ProviderInvocationMetadata, ProviderInvocationRequest } from "./provider_port.js";

export interface NormalizedProviderInvocationRequest {
  providerKey: string;
  fallbackProviderKeys: string[];
  prompt: string;
  metadata: ProviderInvocationMetadata;
}

function normalizePrompt(prompt: string): string {
  return prompt.replace(/\s+/g, " ").trim();
}

function normalizeMetadata(metadata: ProviderInvocationMetadata): ProviderInvocationMetadata {
  return {
    runId: metadata.runId.trim(),
    missionId: metadata.missionId.trim(),
    objective: metadata.objective.trim(),
    taskId: metadata.taskId?.trim() || undefined,
    handoffId: metadata.handoffId?.trim() || undefined,
  };
}

export function normalizeProviderRequest(
  request: ProviderInvocationRequest,
  resolvedProviderKey: string,
): NormalizedProviderInvocationRequest {
  return {
    providerKey: resolvedProviderKey,
    fallbackProviderKeys: request.fallbackProviderKeys?.map((key) => key.trim()).filter(Boolean) ?? [],
    prompt: normalizePrompt(request.prompt),
    metadata: normalizeMetadata(request.metadata),
  };
}
