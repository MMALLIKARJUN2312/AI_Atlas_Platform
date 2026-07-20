"use client";

import { Search, Building2 } from "lucide-react";

interface CompanySearchProps {
  value: string;
  total: number;
  onChange: (value: string) => void;
}

export function CompanySearch({
  value,
  total,
  onChange,
}: CompanySearchProps) {
  return (
    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600/10">
            <Building2
              size={20}
              className="text-blue-500"
            />
          </div>

          <div>
            <h1 className="text-2xl font-semibold text-white">
              Companies
            </h1>

            <p className="text-sm text-zinc-400">
              {total} companies available
            </p>
          </div>
        </div>
      </div>

      <div className="relative w-full max-w-xl lg:w-96">
        <Search
          size={18}
          className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500"
        />

        <input
          value={value}
          onChange={(e) =>
            onChange(e.target.value)
          }
          placeholder="Search companies..."
          className="
            h-11
            w-full
            rounded-lg
            border
            border-zinc-800
            bg-zinc-900
            pl-11
            pr-4
            text-sm
            text-white
            placeholder:text-zinc-500
            outline-none
            transition
            focus:border-sky-400
            focus:ring-2
            focus:ring-sky-400/20
          "
        />
      </div>
    </div>
  );
}
