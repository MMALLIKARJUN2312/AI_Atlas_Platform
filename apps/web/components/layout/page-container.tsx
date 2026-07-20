import { PropsWithChildren } from "react";

import { cn } from "@/lib/utils";

interface PageContainerProps
  extends PropsWithChildren {
  className?: string;
}

export function PageContainer({
  children,
  className,
}: PageContainerProps) {
  return (
    <div
      className={cn(
        "mx-auto w-full max-w-7xl",
        "space-y-8 py-1 sm:space-y-10",
        className
      )}
    >
      {children}
    </div>
  );
}
