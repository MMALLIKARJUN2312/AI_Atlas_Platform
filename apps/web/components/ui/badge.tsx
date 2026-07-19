import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type BadgeVariant =
  | "primary"
  | "secondary"
  | "success"
  | "warning"
  | "danger";

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

const variants = {
  primary:
    "border-cyan-400/20 bg-cyan-400/10 text-cyan-300",

  secondary:
    "border-white/10 bg-white/5 text-zinc-300",

  success:
    "border-emerald-400/20 bg-emerald-400/10 text-emerald-300",

  warning:
    "border-amber-400/20 bg-amber-400/10 text-amber-300",

  danger:
    "border-red-400/20 bg-red-400/10 text-red-300",
};

export function Badge({
  className,
  variant = "secondary",
  children,
  ...props
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center justify-center rounded-full",
        "border px-3 py-1",
        "text-xs font-medium",
        "tracking-wide",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}