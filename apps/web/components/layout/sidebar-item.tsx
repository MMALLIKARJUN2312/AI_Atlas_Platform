"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LucideIcon } from "lucide-react";

import { cn } from "@/lib/utils";

interface SidebarItemProps {
  href: string;
  label: string;
  icon: LucideIcon;
  collapsed?: boolean;
}

export function SidebarItem({
  href,
  label,
  icon: Icon,
  collapsed = false,
}: SidebarItemProps) {
  const pathname = usePathname();

  const active =
    href === "/" ? pathname === "/" : pathname === href || pathname.startsWith(`${href}/`);

  return (
    <Link
      href={href}
      title={collapsed ? label : undefined}
      aria-current={active ? "page" : undefined}
      className={cn(
        "flex h-12 items-center gap-3.5 rounded-lg px-3.5 text-sm font-medium transition-colors",
        collapsed && "justify-center px-0",
        active
          ? "bg-blue-600 text-white"
          : "text-zinc-400 hover:bg-zinc-800 hover:text-white"
      )}
    >
      <Icon size={19} className="shrink-0" />

      {!collapsed && <span className="truncate">{label}</span>}
    </Link>
  );
}
