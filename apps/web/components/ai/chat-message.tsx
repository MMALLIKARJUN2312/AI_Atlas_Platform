import { Bot, User } from "lucide-react";

import { CitationList } from "./citation-list";
import type { ChatMessage as ChatMessageType } from "@/types/ai";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === "assistant";

  return (
    <article className={`flex gap-3 ${isAssistant ? "justify-start" : "justify-end"}`}>
      {isAssistant ? <MessageIcon assistant /> : null}
      <div
        className={`max-w-3xl rounded-2xl px-5 py-4 text-sm leading-6 ${isAssistant ? "border border-white/10 bg-white/[0.04] text-zinc-200" : "bg-cyan-400 text-slate-950"}`}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>
        {isAssistant ? <CitationList sources={message.sources ?? []} /> : null}
      </div>
      {!isAssistant ? <MessageIcon /> : null}
    </article>
  );
}

function MessageIcon({ assistant = false }: { assistant?: boolean }) {
  return (
    <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${assistant ? "bg-cyan-400/15 text-cyan-300" : "bg-zinc-800 text-zinc-200"}`}>
      {assistant ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
    </div>
  );
}
