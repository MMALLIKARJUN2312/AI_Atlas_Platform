import { ReactNode } from "react";

import { cn } from "@/lib/utils";
import { GlassPanel } from "./glass-panel";

export interface EmptyStateProps {
  title: string;
  description: string;
  icon?: ReactNode;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({
  title,
  description,
  icon,
  action,
  className,
}: EmptyStateProps) {
  return (
    <GlassPanel
      className={cn(
        "flex flex-col items-center justify-center",
        "px-8 py-14 text-center",
        className
      )}
    >
      {icon && (
        <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-300">
          {icon}
        </div>
      )}

      <h3 className="text-xl font-semibold text-white">
        {title}
      </h3>

      <p className="mt-3 max-w-md text-sm leading-6 text-zinc-400">
        {description}
      </p>

      {action && <div className="mt-8">{action}</div>}
    </GlassPanel>
  );
}