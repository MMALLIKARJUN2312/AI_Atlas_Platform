import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

export type LoadingSkeletonProps = HTMLAttributes<HTMLDivElement>;

export function LoadingSkeleton({ className, ...props }: LoadingSkeletonProps) {
  return (
    <div
      className={cn(
        "animate-pulse rounded-xl",
        "bg-gradient-to-r",
        "from-white/5",
        "via-white/10",
        "to-white/5",
        className,
      )}
      {...props}
    />
  );
}
