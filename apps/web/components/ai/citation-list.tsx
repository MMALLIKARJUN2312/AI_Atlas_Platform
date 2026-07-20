import Link from "next/link";
import { ExternalLink, FileText } from "lucide-react";

import type { AISource } from "@/types/ai";

interface CitationListProps {
  sources: AISource[];
}

export function CitationList({ sources }: CitationListProps) {
  if (sources.length === 0) return null;

  return (
    <div className="mt-4 border-t border-white/10 pt-4">
      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-zinc-500">Sources</p>
      <div className="flex flex-wrap gap-2">
        {sources.map((source) => (
          <div
            key={source.chunk_id}
            className="flex items-center gap-2 rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-sm text-zinc-300"
          >
            <FileText className="h-3.5 w-3.5 shrink-0 text-cyan-300" />
            {source.company_id ? (
              <Link href={`/companies/${source.company_id}`} className="hover:text-cyan-300">
                {source.title}
              </Link>
            ) : (
              <span>{source.title}</span>
            )}
            <span className="text-xs text-zinc-500">{source.source_type}</span>
            {source.url ? (
              <a
                href={source.url}
                target="_blank"
                rel="noreferrer"
                aria-label={`Open ${source.title} source`}
                className="text-zinc-500 hover:text-cyan-300"
              >
                <ExternalLink className="h-3.5 w-3.5" />
              </a>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}
