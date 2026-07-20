import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export type DividerProps = HTMLAttributes<HTMLHRElement>;

export function Divider({ className, ...props }: DividerProps) {
  return (
    <hr
      className={cn(
        "border-0",
        "h-px",
        "w-full",
        "bg-gradient-to-r",
        "from-transparent",
        "via-white/10",
        "to-transparent",
        className,
      )}
      {...props}
    />
  );
}
