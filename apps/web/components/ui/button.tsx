import * as React from "react";
import { Slot } from "@radix-ui/react-slot";

import { cn } from "@/lib/utils";

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
}

export function Button({
  asChild,
  className,
  ...props
}: ButtonProps) {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      className={cn(
        `
        inline-flex
        items-center
        justify-center
        gap-2
        rounded-lg
        bg-sky-400
        px-4
        py-2.5
        font-medium
        text-slate-950
        transition-all
        duration-300
        hover:bg-sky-300
        focus-visible:outline-none
        focus-visible:ring-2
        focus-visible:ring-sky-300
        focus-visible:ring-offset-2
        focus-visible:ring-offset-zinc-950
        `,
        className
      )}
      {...props}
    />
  );
}
