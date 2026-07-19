import { ButtonHTMLAttributes, forwardRef } from "react";

import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
}

const variants: Record<ButtonVariant, string> = {
  primary:
    "bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-lg hover:scale-[1.02] hover:shadow-cyan-500/30",

  secondary:
    "border border-white/15 bg-white/5 text-white hover:bg-white/10",

  ghost:
    "text-zinc-300 hover:bg-white/5",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex h-11 items-center justify-center rounded-xl px-5 text-sm font-semibold transition-all duration-200 disabled:pointer-events-none disabled:opacity-50",
        variants[variant],
        className,
      )}
      {...props}
    />
  ),
);

Button.displayName = "Button";