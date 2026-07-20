import * as React from "react";

import { cn } from "@/lib/utils";

export const Input = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>((props, ref) => {
  return (
    <input
      ref={ref}
      className={cn(
        `
        h-14
        w-full
        rounded-2xl
        border
        border-white/10
        bg-white/[0.04]
        px-5
        text-white
        placeholder:text-slate-500
        backdrop-blur-xl
        transition-all
        focus:border-cyan-400
        focus:ring-4
        focus:ring-cyan-400/20
        outline-none
        `,
        props.className
      )}
      {...props}
    />
  );
});

Input.displayName = "Input";