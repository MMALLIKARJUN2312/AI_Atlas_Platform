"use client";

import { useState } from "react";
import { ChevronDown, Wrench } from "lucide-react";

import type { AgentStep } from "@/types/ai";

interface ReasoningTraceProps {
  steps: AgentStep[];
}

/** Shows the agent's real tool calls for this answer - not a simulated "thinking" animation. */
export function ReasoningTrace({ steps }: ReasoningTraceProps) {
  const [open, setOpen] = useState(false);

  if (steps.length === 0) return null;

  return (
    <div className="mt-4 border-t border-white/10 pt-4">
      <button
        type="button"
        onClick={() => setOpen((current) => !current)}
        className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500 hover:text-cyan-300"
      >
        <Wrench className="h-3.5 w-3.5" />
        Reasoning ({steps.length} step{steps.length === 1 ? "" : "s"})
        <ChevronDown className={`h-3.5 w-3.5 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>

      {open ? (
        <ol className="mt-3 space-y-2">
          {steps.map((step) => (
            <li key={step.step} className="rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-xs text-zinc-400">
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-full bg-cyan-400/10 px-2 py-0.5 font-mono text-cyan-300">{step.tool}</span>
                {Object.entries(step.arguments).map(([key, value]) => (
                  <span key={key} className="text-zinc-500">
                    {key}: <span className="text-zinc-300">{String(value)}</span>
                  </span>
                ))}
              </div>
              <p className="mt-1.5 line-clamp-2 whitespace-pre-wrap text-zinc-500">{step.observation}</p>
            </li>
          ))}
        </ol>
      ) : null}
    </div>
  );
}
