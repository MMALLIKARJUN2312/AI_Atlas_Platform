"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

interface SidebarItemProps {
  href: string;
  label: string;
  icon: LucideIcon;
}

export function SidebarItem({
  href,
  label,
  icon: Icon,
}: SidebarItemProps) {
  const pathname = usePathname();

  const active =
    pathname === href ||
    pathname.startsWith(`${href}/`);

  return (
    <Link
      href={href}
      className={cn(
        "flex items-center gap-3 rounded-2xl px-4 py-3",
        "transition-all duration-200",
        active
          ? "bg-cyan-400/10 text-cyan-300"
          : "text-zinc-400 hover:bg-white/5 hover:text-white"
      )}
    >
      <Icon size={18} />

      <span className="text-sm font-medium">
        {label}
      </span>
    </Link>
  );
}