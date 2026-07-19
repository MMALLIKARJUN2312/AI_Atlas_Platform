import { ReactNode } from "react";

import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";
import { PageContainer } from "./page-container";

type Props = {
  children: ReactNode;
};

export function AppShell({
  children,
}: Props) {
  return (
    <div className="min-h-screen bg-[#050816]">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,#1e40af22,transparent_60%)]" />
      <div className="relative grid min-h-screen grid-cols-[290px_1fr] gap-6 p-6">
        <Sidebar />
        <div>
          <Topbar />
          <PageContainer>
            {children}
          </PageContainer>
        </div>
      </div>
    </div>
  );
}