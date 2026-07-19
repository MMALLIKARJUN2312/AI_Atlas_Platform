import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";
import { GlassPanel } from "./glass-panel";

interface CardProps extends HTMLAttributes<HTMLDivElement> {}

export function Card({
  className,
  children,
  ...props
}: CardProps) {
  return (
    <GlassPanel
      className={cn(
        "group p-6",
        "hover:-translate-y-1",
        "hover:border-cyan-400/20",
        "hover:shadow-[0_30px_80px_rgba(34,211,238,0.10)]",
        className
      )}
      {...props}
    >
      {children}
    </GlassPanel>
  );
}