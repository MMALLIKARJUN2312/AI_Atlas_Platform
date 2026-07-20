import * as React from "react";
import { Slot } from "@radix-ui/react-slot";

import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary" | "danger";

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
  variant?: ButtonVariant;
}

const base = `
  inline-flex
  items-center
  justify-center
  gap-2
  rounded-lg
  px-4
  py-2.5
  font-medium
  transition-all
  duration-200
  focus-visible:outline-none
  focus-visible:ring-2
  focus-visible:ring-offset-2
  focus-visible:ring-offset-zinc-950
  disabled:pointer-events-none
  disabled:opacity-50
`;

const variants: Record<ButtonVariant, string> = {
  primary: "bg-sky-400 text-slate-950 hover:bg-sky-300 focus-visible:ring-sky-300",
  secondary: "border border-white/10 text-zinc-300 hover:border-cyan-400/40 hover:text-cyan-300 focus-visible:ring-cyan-400/60",
  danger: "border border-red-400/30 text-red-300 hover:border-red-400/60 hover:bg-red-400/10 focus-visible:ring-red-400/60",
};

export function Button({
  asChild,
  variant = "primary",
  className,
  ...props
}: ButtonProps) {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      className={cn(base, variants[variant], className)}
      {...props}
    />
  );
}
