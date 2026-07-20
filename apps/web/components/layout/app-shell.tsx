"use client";

import { ReactNode, useState } from "react";
import { usePathname } from "next/navigation";

import { AppBackground } from "./app-background";
import { MobileSidebar } from "./mobile-sidebar";
import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";

interface Props {
  children: ReactNode;
}

export function AppShell({
  children,
}: Props) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();

  // Close the mobile drawer whenever the route changes, without an effect
  // (React's documented pattern for adjusting state in response to a prop/
  // external change: compare against the previous render, update during render).
  const [lastPathname, setLastPathname] = useState(pathname);
  if (pathname !== lastPathname) {
    setLastPathname(pathname);
    setMobileOpen(false);
  }

  return (
    <AppBackground>
      <div className="flex min-h-screen">
        <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((value) => !value)} />

        <MobileSidebar open={mobileOpen} onClose={() => setMobileOpen(false)} />

        <div className="flex min-h-screen min-w-0 flex-1 flex-col">
          <Topbar onMenuClick={() => setMobileOpen(true)} />

          <main className="min-w-0 flex-1 px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
            {children}
          </main>
        </div>
      </div>
    </AppBackground>
  );
}
