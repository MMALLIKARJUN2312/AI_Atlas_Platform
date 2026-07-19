import {
  ButtonHTMLAttributes,
  forwardRef,
} from "react";

import { cn } from "@/lib/utils";

export interface IconButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {}

export const IconButton = forwardRef<
  HTMLButtonElement,
  IconButtonProps
>(({ className, children, ...props }, ref) => {
  return (
    <button
      ref={ref}
      className={cn(
        "inline-flex h-11 w-11 items-center justify-center rounded-xl",
        "border border-white/10",
        "bg-white/5",
        "text-zinc-200",
        "transition-all duration-200",
        "hover:border-cyan-400/30",
        "hover:bg-white/10",
        "hover:text-white",
        "focus:outline-none focus:ring-2 focus:ring-cyan-400",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
});

IconButton.displayName = "IconButton";