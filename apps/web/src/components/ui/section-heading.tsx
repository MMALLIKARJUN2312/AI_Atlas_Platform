import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

interface Props extends HTMLAttributes<HTMLDivElement> {
  title: string;
  subtitle?: string;
}

export function SectionHeading({
  title,
  subtitle,
  className,
}: Props) {
  return (
    <div className={cn(className)}>
      <h2 className="text-3xl font-bold tracking-tight text-white">
        {title}
      </h2>

      {subtitle && (
        <p className="mt-2 text-zinc-400">
          {subtitle}
        </p>
      )}
    </div>
  );
}