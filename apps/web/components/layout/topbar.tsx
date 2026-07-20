"use client";

import Link from "next/link";
import { Bell, BrainCircuit } from "lucide-react";

export function Topbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-zinc-800 bg-[#111113]/95 backdrop-blur">
      <div className="flex h-16 items-center justify-between px-6 lg:px-8">
        {/* Left */}

        <div className="flex items-center gap-4">
          <div className="hidden text-sm text-zinc-500 md:block">
            AI Atlas Platform
          </div>
        </div>

        {/* Right */}

        <div className="flex items-center gap-3">
          <Link href="/ask-ai" className="flex items-center gap-2 rounded-lg bg-red px-3 py-2 text-sm font-medium text-zinc-950 transition hover:bg-zinc-200">
            <BrainCircuit size={18} />
            <span className="hidden sm:inline">Ask AI</span>
          </Link>

          <button className="rounded-lg border border-zinc-800 bg-zinc-900 p-2.5 text-zinc-400 transition hover:border-zinc-700 hover:text-white">
            <Bell size={18} />
          </button>

          <div className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-2 py-1.5 sm:px-3 sm:py-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white">
              M
            </div>

            <div className="hidden md:block">
              <p className="text-sm font-medium text-white">
                Mallikarjun
              </p>

              <p className="text-xs text-zinc-500">
                AI Engineer
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
