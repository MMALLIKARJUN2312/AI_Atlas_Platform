import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

interface GlassPanelProps extends HTMLAttributes<HTMLDivElement> {}

export function GlassPanel({
  className,
  children,
  ...props
}: GlassPanelProps) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-3xl",
        "border border-white/10",
        "bg-white/[0.04]",
        "backdrop-blur-2xl",
        "shadow-[0_24px_60px_rgba(0,0,0,0.45)]",
        "transition-all duration-300",
        className
      )}
      {...props}
    >
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-cyan-400/5" />

      <div className="relative">{children}</div>
    </div>
  );
}