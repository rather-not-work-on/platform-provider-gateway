export interface ProviderInvocationMetadata {
  runId: string;
  missionId: string;
  objective: string;
  taskId?: string;
  handoffId?: string;
}

export interface ProviderInvocationRequest {
  providerKey?: string;
  fallbackProviderKeys?: string[];
  prompt: string;
  metadata: ProviderInvocationMetadata;
}

export interface ProviderInvocationResult {
  resultType: "complete" | "partial" | "failed" | "canceled";
  reasonCode: string;
  providerKey?: string;
  normalizedPrompt?: string;
  outputText?: string;
}
