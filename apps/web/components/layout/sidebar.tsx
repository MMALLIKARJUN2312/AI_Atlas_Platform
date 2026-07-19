"use client";

import {
  Building2,
  LayoutDashboard,
  MessageSquare,
  Newspaper,
  Shield,
} from "lucide-react";

import { Card } from "@/components/ui";
import { Logo } from "./logo";
import { SidebarItem } from "./sidebar-item";

export function Sidebar() {
  return (
    <Card className="flex h-full w-72 flex-col p-6">

      <Logo />

      <div className="mt-10 flex flex-col gap-2">

        <SidebarItem
          href="/"
          label="Dashboard"
          icon={LayoutDashboard}
          active
        />

        <SidebarItem
          href="/companies"
          label="Companies"
          icon={Building2}
        />

        <SidebarItem
          href="/ask-ai"
          label="Ask AI"
          icon={MessageSquare}
        />

        <SidebarItem
          href="/news"
          label="News"
          icon={Newspaper}
        />

        <SidebarItem
          href="/admin"
          label="Admin"
          icon={Shield}
        />

      </div>

    </Card>
  );
}