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

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: AISource[];
}
