"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BrainCircuit, Menu } from "lucide-react";

interface TopbarProps {
  onMenuClick?: () => void;
}

function pageTitle(pathname: string): string {
  if (pathname === "/") return "Dashboard";
  if (pathname === "/companies") return "Companies";
  if (pathname.startsWith("/companies/")) return "Company Profile";
  if (pathname === "/ask-ai") return "Ask AI";
  if (pathname === "/admin") return "Admin";
  if (pathname === "/admin/companies") return "Data Management";
  if (pathname === "/admin/login") return "Admin Sign In";
  return "AI Atlas";
}

export function Topbar({ onMenuClick }: TopbarProps) {
  const pathname = usePathname();
  const onAskAI = pathname === "/ask-ai";

  return (
    <header className="sticky top-0 z-30 border-b border-zinc-800 bg-[#111113]/95 backdrop-blur">
      <div className="flex h-20 items-center justify-between gap-3 px-4 sm:px-6 lg:px-8">
        <div className="flex min-w-0 items-center gap-4">
          <button
            type="button"
            onClick={onMenuClick}
            aria-label="Open navigation"
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-zinc-800 bg-zinc-900 text-zinc-300 transition hover:border-zinc-700 hover:text-white lg:hidden"
          >
            <Menu size={18} />
          </button>

          <h1 className="truncate text-xl font-semibold tracking-tight text-white">
            {pageTitle(pathname)}
          </h1>
        </div>

        <div className="flex shrink-0 items-center gap-4">
          {!onAskAI && (
            <Link
              href="/ask-ai"
              className="flex items-center gap-2 rounded-lg bg-sky-400 px-4 py-2.5 text-sm font-medium text-slate-950 transition hover:bg-sky-300"
            >
              <BrainCircuit size={18} />
              <span className="hidden sm:inline">Ask AI</span>
            </Link>
          )}

          <div className="flex items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white">
              A
            </div>

            <div className="hidden md:block">
              <p className="text-sm font-medium leading-tight text-white">
                Admin
              </p>

              <p className="text-xs leading-tight text-zinc-500">
                AI Atlas
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
