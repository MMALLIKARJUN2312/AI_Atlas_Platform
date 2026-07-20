"use client";

import {
  Brain,
  Building2,
  LayoutDashboard,
  Layers3,
  Lightbulb,
  ShieldCheck,
} from "lucide-react";

import { Logo } from "./logo";
import { SidebarItem } from "./sidebar-item";

const navigation = [
  {
    label: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    label: "Companies",
    href: "/companies",
    icon: Building2,
  },
  {
    label: "Ask AI",
    href: "/ask-ai",
    icon: Brain,
  },
  {
    label: "Admin",
    href: "/admin",
    icon: ShieldCheck,
  },
];

export function Sidebar() {
  return (
    <aside className="hidden w-[260px] shrink-0 border-r border-zinc-800 bg-[#111113] lg:flex lg:flex-col">
      <div className="border-b border-zinc-800 px-6 py-6">
        <Logo />
      </div>

      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => (
          <SidebarItem
            key={item.href}
            {...item}
          />
        ))}
      </nav>

      <div className="border-t border-zinc-800 p-5">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 font-semibold text-white">
            M
          </div>

          <div>
            <p className="text-sm font-medium text-white">
              Mallikarjun
            </p>

            <p className="text-xs text-zinc-400">
              AI Engineer
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
