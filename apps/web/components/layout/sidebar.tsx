"use client";

import { navigation } from "@/lib/navigation";

import { GlassPanel } from "@/components/ui";
import {Logo} from "./logo";
import { SidebarItem } from "./sidebar-item";

export function Sidebar() {
  return (
    <GlassPanel
      className="
        sticky
        top-6
        flex
        h-[calc(100vh-48px)]
        w-72
        flex-col
        p-6
      "
    >
      <Logo />

      <nav className="mt-10 space-y-2">
        {navigation.map((item) => (
          <SidebarItem
            key={item.href}
            {...item}
          />
        ))}
      </nav>

      <div className="mt-auto">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="text-xs uppercase tracking-widest text-zinc-500">
            Version
          </p>

          <p className="mt-2 text-sm font-medium text-white">
            Build v1.0
          </p>
        </div>
      </div>
    </GlassPanel>
  );
}