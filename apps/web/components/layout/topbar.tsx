import { Search } from "lucide-react";

import { Input } from "@/components/ui";

export function Topbar() {
  return (
    <header className="flex h-20 items-center justify-between">

      <div className="w-96">

        <div className="relative">

          <Search
            className="absolute left-4 top-3 text-zinc-500"
            size={18}
          />

          <Input
            className="pl-11"
            placeholder="Search companies..."
          />

        </div>

      </div>

      <div className="rounded-full border border-cyan-500/20 bg-cyan-500/10 px-4 py-2 text-sm text-cyan-300">
        AI Powered
      </div>

    </header>
  );
}