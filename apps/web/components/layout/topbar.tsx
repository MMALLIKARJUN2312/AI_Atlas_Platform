"use client";

import { Menu } from "lucide-react";

import { IconButton, SearchInput } from "@/components/ui";

interface TopbarProps {
  onMenuClick: () => void;
}

export function Topbar({
  onMenuClick,
}: TopbarProps) {
  return (
    <header className="sticky top-0 z-30 mb-10 flex items-center justify-between gap-6 backdrop-blur-xl">
      <div className="lg:hidden">
        <IconButton
          onClick={onMenuClick}
          aria-label="Open navigation"
        >
          <Menu size={18} />
        </IconButton>
      </div>

      <div className="ml-auto w-full max-w-xl">
        <SearchInput placeholder="Search companies..." />
      </div>
    </header>
  );
}