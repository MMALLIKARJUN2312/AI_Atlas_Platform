import { apiClient } from "@/lib/api-client";
import type { AskAIResponse } from "@/types/ai";

class AIService {
  async ask(question: string) {
    const { data } = await apiClient.post<AskAIResponse>("/ai/ask", { question });
    return data;
  }
}

export const aiService = new AIService();
