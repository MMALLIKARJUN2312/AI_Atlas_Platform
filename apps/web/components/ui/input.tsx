import {
  forwardRef,
  InputHTMLAttributes,
} from "react";

import { cn } from "@/lib/utils";

export interface InputProps
  extends InputHTMLAttributes<HTMLInputElement> {}

export const Input = forwardRef<
  HTMLInputElement,
  InputProps
>(({ className, ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={cn(
        "h-12 w-full rounded-2xl",
        "border border-white/10",
        "bg-white/5",
        "px-4",
        "text-sm text-white",
        "placeholder:text-zinc-500",
        "outline-none",
        "transition-all duration-200",
        "focus:border-cyan-400/40",
        "focus:ring-2 focus:ring-cyan-400/20",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  );
});

Input.displayName = "Input";