import Link from "next/link";
import { Boxes } from "lucide-react";

export function Logo() {
  return (
    <Link
      href="/"
      className="flex items-center gap-3"
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10 text-cyan-300">
        <Boxes size={22} />
      </div>

      <div>
        <h1 className="text-lg font-bold tracking-tight text-white">
          AI Atlas
        </h1>

        <p className="text-xs text-zinc-500">
          German Food Intelligence
        </p>
      </div>
    </Link>
  );
}