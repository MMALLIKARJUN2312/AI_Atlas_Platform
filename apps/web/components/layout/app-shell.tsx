"use client";

import { PropsWithChildren, useState } from "react";

import { AppBackground } from "./app-background";
import { MobileSidebar } from "./mobile-sidebar";
import { PageContainer } from "./page-container";
import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";

export function AppShell({
  children,
}: PropsWithChildren) {
  const [mobileMenuOpen, setMobileMenuOpen] =
    useState(false);

  return (
    <>
      <AppBackground />

      <MobileSidebar
        open={mobileMenuOpen}
        onClose={() =>
          setMobileMenuOpen(false)
        }
      />

      <div className="relative z-10 flex min-h-screen">
        <aside className="hidden shrink-0 p-6 lg:block">
          <Sidebar />
        </aside>

        <div className="min-w-0 flex-1">
          <PageContainer>
            <Topbar
              onMenuClick={() =>
                setMobileMenuOpen(true)
              }
            />

            {children}
          </PageContainer>
        </div>
      </div>
    </>
  );
}