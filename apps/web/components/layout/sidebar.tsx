"use client";

import {
  Brain,
  Building2,
  LayoutDashboard,
  PanelLeftClose,
  PanelLeftOpen,
  ShieldCheck,
} from "lucide-react";

import { cn } from "@/lib/utils";
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

interface SidebarProps {
  collapsed?: boolean;
  onToggle?: () => void;
  /** Renders as a plain flex column regardless of viewport - used inside the mobile drawer. */
  forceVisible?: boolean;
}

export function Sidebar({ collapsed = false, onToggle, forceVisible = false }: SidebarProps) {
  return (
    <aside
      className={cn(
        "shrink-0 border-r border-zinc-800 bg-[#111113] transition-[width] duration-200",
        forceVisible ? "flex h-full w-full flex-col" : "hidden lg:flex lg:flex-col",
        !forceVisible && (collapsed ? "lg:w-[76px]" : "lg:w-[260px]"),
      )}
    >
      <div className="flex h-20 items-center gap-2 border-b border-zinc-800 px-5">
        {collapsed ? (
          <div className="mx-auto flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-white">
            <Brain size={20} />
          </div>
        ) : (
          <Logo />
        )}
      </div>

      <nav className="flex-1 space-y-1.5 p-4">
        {navigation.map((item) => (
          <SidebarItem
            key={item.href}
            {...item}
            collapsed={collapsed}
          />
        ))}
      </nav>

      {onToggle ? (
        <div className="border-t border-zinc-800 p-4">
          <button
            type="button"
            onClick={onToggle}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            className={cn(
              "flex h-11 w-full items-center gap-3 rounded-lg px-3 text-sm font-medium text-zinc-400 transition-colors hover:bg-zinc-800 hover:text-white",
              collapsed && "justify-center",
            )}
          >
            {collapsed ? <PanelLeftOpen size={18} /> : <PanelLeftClose size={18} />}
            {!collapsed && <span>Collapse</span>}
          </button>
        </div>
      ) : null}

      <div className={cn("border-t border-zinc-800 p-4", collapsed && "px-3")}>
        <div className={cn("flex items-center gap-3", collapsed && "justify-center")}>
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-600 font-semibold text-white">
            A
          </div>

          {!collapsed && (
            <div className="min-w-0">
              <p className="truncate text-sm font-medium leading-tight text-white">
                Admin
              </p>

              <p className="truncate text-xs leading-tight text-zinc-400">
                AI Atlas
              </p>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
