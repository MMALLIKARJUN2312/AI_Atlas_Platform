"use client";

import Link from "next/link";
import { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

type Props = {
  href: string;
  label: string;
  icon: LucideIcon;
  active?: boolean;
};

export function SidebarItem({
  href,
  icon: Icon,
  label,
  active,
}: Props) {
  return (
    <Link
      href={href}
      className={cn(
        "flex items-center gap-3 rounded-xl px-4 py-3 text-sm transition-all",
        active
          ? "bg-cyan-500/20 text-cyan-300"
          : "text-zinc-400 hover:bg-white/5 hover:text-white",
      )}
    >
      <Icon size={18} />
      {label}
    </Link>
  );
}