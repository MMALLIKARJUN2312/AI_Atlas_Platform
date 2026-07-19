import { Bot } from "lucide-react";

export function Logo() {
  return (
    <div className="flex items-center gap-3">
      <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/30">
        <Bot className="h-6 w-6 text-white" />
      </div>

      <div>
        <h1 className="text-lg font-bold text-white">
          AI Atlas
        </h1>

        <p className="text-xs text-zinc-400">
          Intelligence Platform
        </p>
      </div>
    </div>
  );
}