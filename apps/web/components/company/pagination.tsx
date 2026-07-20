"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";

interface Props {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ page, totalPages, onPageChange }: Props) {
  if (totalPages <= 1) {
    return null;
  }

  return (
    <nav
      className="mt-10 flex items-center justify-center gap-2"
      aria-label="Company directory pages"
    >
      <button
        type="button"
        onClick={() => onPageChange(page - 1)}
        disabled={page === 1}
        className="flex h-10 items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-4 text-sm text-zinc-300 transition hover:border-zinc-700 hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <ChevronLeft size={16} />
        Previous
      </button>

      {Array.from({ length: totalPages }).map((_, index) => {
        const current = index + 1;

        return (
          <button
            type="button"
            key={current}
            onClick={() => onPageChange(current)}
            aria-current={current === page ? "page" : undefined}
            className={`h-10 w-10 rounded-lg border text-sm font-medium transition ${
              current === page
                ? "border-blue-500 bg-blue-600 text-white"
                : "border-zinc-800 bg-zinc-900 text-zinc-300 hover:border-zinc-700 hover:bg-zinc-800"
            }`}
          >
            {current}
          </button>
        );
      })}

      <button
        type="button"
        onClick={() => onPageChange(page + 1)}
        disabled={page === totalPages}
        className="flex h-10 items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-4 text-sm text-zinc-300 transition hover:border-zinc-700 hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Next
        <ChevronRight size={16} />
      </button>
    </nav>
  );
}
