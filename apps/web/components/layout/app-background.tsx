"use client";

import { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

export function AppBackground({
  children,
}: Props) {
  return (
    <div className="min-h-screen bg-[#09090B] text-white">
      {children}
    </div>
  );
}