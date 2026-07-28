export interface AISource {
  title: string;
  source_type: string;
  company_id: number | null;
  url: string | null;
  chunk_id: string;
}

export interface AskAIResponse {
  answer: string;
  sources: AISource[];
}

export interface AgentStep {
  step: number;
  tool: string;
  arguments: Record<string, unknown>;
  observation: string;
  metadata: Record<string, unknown>;
}

export interface AgentResponse {
  answer: string;
  sources: AISource[];
  steps: AgentStep[];
  tools_used: string[];
  iterations: number;
  grounded: boolean;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: AISource[];
  steps?: AgentStep[];
  toolsUsed?: string[];
}
