import { apiClient } from "@/lib/api-client";
import type { AgentResponse, AskAIResponse } from "@/types/ai";

class AIService {
  /** Legacy single-shot RAG endpoint - kept for reference, no longer used by the chat UI. */
  async ask(question: string) {
    const { data } = await apiClient.post<AskAIResponse>("/ai/ask", { question });
    return data;
  }

  async askAgent(question: string) {
    const { data } = await apiClient.post<AgentResponse>("/agent/ask", { question });
    return data;
  }
}

export const aiService = new AIService();
