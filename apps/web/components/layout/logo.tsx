import Link from "next/link";
import { BrainCircuit } from "lucide-react";

export function Logo() {
  return (
    <Link
      href="/"
      className="flex items-center gap-3"
    >
      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
        <BrainCircuit size={20} />
      </div>

      <div className="min-w-0">
        <h1 className="text-lg font-semibold tracking-tight text-white">
          AI Atlas
        </h1>

        <p className="text-xs text-zinc-400">
          Intelligence Platform
        </p>
      </div>
    </Link>
  );
}