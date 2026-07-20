"use client";

import { type FormEvent, useState } from "react";
import { ArrowUp, Bot, LoaderCircle } from "lucide-react";

import { Button, Card } from "@/components/ui";
import { useAskAI } from "@/hooks";
import type { ChatMessage } from "@/types/ai";

import { ChatMessage as ChatMessageItem } from "./chat-message";

export function AskAIPanel() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const askAI = useAskAI();

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const submittedQuestion = question.trim();
    if (!submittedQuestion || askAI.isPending) return;

    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", content: submittedQuestion },
    ]);
    setQuestion("");

    try {
      const response = await askAI.mutateAsync(submittedQuestion);
      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "assistant", content: response.answer, sources: response.sources },
      ]);
    } catch {
      // The visible error state below provides a recoverable response without losing the conversation.
    }
  }

  return (
    <Card className="mx-auto flex min-h-[620px] max-w-5xl flex-col p-0 hover:translate-y-0">
      <div className="border-b border-white/10 px-6 py-5 sm:px-8">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-cyan-400/15 p-2 text-cyan-300"><Bot className="h-5 w-5" /></div>
          <div>
            <h1 className="text-xl font-semibold text-white">Ask AI Atlas</h1>
            <p className="text-sm text-zinc-400">Grounded answers across German food and beverage AI intelligence.</p>
          </div>
        </div>
      </div>

      <div className="flex-1 space-y-5 overflow-y-auto px-6 py-8 sm:px-8" aria-live="polite">
        {messages.length === 0 ? (
          <div className="mx-auto max-w-xl pt-20 text-center">
            <Bot className="mx-auto h-10 w-10 text-cyan-300" />
            <h2 className="mt-5 text-lg font-semibold text-white">What would you like to explore?</h2>
            <p className="mt-2 text-sm text-zinc-400">Ask about companies, the problems they solve, market sectors, or recent news.</p>
          </div>
        ) : (
          messages.map((message) => <ChatMessageItem key={message.id} message={message} />)
        )}
        {askAI.isPending ? (
          <div className="flex items-center gap-3 text-sm text-zinc-400"><LoaderCircle className="h-4 w-4 animate-spin text-cyan-300" /> Researching the knowledge base…</div>
        ) : null}
        {askAI.isError ? <p className="rounded-xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-200">Your question could not be answered. Please try again.</p> : null}
      </div>

      <form onSubmit={handleSubmit} className="border-t border-white/10 p-4 sm:p-6">
        <div className="flex items-end gap-3 rounded-2xl border border-white/10 bg-black/20 p-2 focus-within:border-cyan-400/50">
          <textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows={2} placeholder="Ask about a company, a problem, or recent news…" className="min-h-12 flex-1 resize-none bg-transparent px-3 py-2 text-sm text-white outline-none placeholder:text-zinc-500" aria-label="Ask AI a question" />
          <Button type="submit" disabled={!question.trim() || askAI.isPending} className="h-11 w-11 rounded-xl px-0 disabled:cursor-not-allowed disabled:opacity-50" aria-label="Send question"><ArrowUp className="h-5 w-5" /></Button>
        </div>
      </form>
    </Card>
  );
}
