"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";

import { cn } from "@/lib/utils";

interface Props {
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

type PageItem = number | "ellipsis-start" | "ellipsis-end";

function getPageItems(page: number, totalPages: number): PageItem[] {
  if (totalPages <= 7) {
    return Array.from({ length: totalPages }, (_, index) => index + 1);
  }

  const items: PageItem[] = [1];

  if (page > 3) items.push("ellipsis-start");

  for (let candidate = Math.max(2, page - 1); candidate <= Math.min(totalPages - 1, page + 1); candidate++) {
    items.push(candidate);
  }

  if (page < totalPages - 2) items.push("ellipsis-end");

  items.push(totalPages);

  return items;
}

export function Pagination({ page, totalPages, onPageChange }: Props) {
  if (totalPages <= 1) {
    return null;
  }

  return (
    <nav
      className="mt-12 flex flex-col items-center gap-3"
      aria-label="Company directory pages"
    >
      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={() => onPageChange(page - 1)}
          disabled={page === 1}
          aria-label="Previous page"
          className="flex h-10 items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-4 text-sm text-zinc-300 transition hover:border-zinc-700 hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <ChevronLeft size={16} />
          <span className="hidden sm:inline">Previous</span>
        </button>

        <div className="flex items-center gap-1.5">
          {getPageItems(page, totalPages).map((item) =>
            typeof item === "number" ? (
              <button
                type="button"
                key={item}
                onClick={() => onPageChange(item)}
                aria-current={item === page ? "page" : undefined}
                className={cn(
                  "h-10 w-10 rounded-lg border text-sm font-medium transition",
                  item === page
                    ? "border-blue-500 bg-blue-600 text-white"
                    : "border-zinc-800 bg-zinc-900 text-zinc-300 hover:border-zinc-700 hover:bg-zinc-800",
                )}
              >
                {item}
              </button>
            ) : (
              <span key={item} className="flex h-10 w-6 items-center justify-center text-zinc-600">
                &hellip;
              </span>
            ),
          )}
        </div>

        <button
          type="button"
          onClick={() => onPageChange(page + 1)}
          disabled={page === totalPages}
          aria-label="Next page"
          className="flex h-10 items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-4 text-sm text-zinc-300 transition hover:border-zinc-700 hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <span className="hidden sm:inline">Next</span>
          <ChevronRight size={16} />
        </button>
      </div>

      <p className="text-xs text-zinc-500">Page {page} of {totalPages}</p>
    </nav>
  );
}
