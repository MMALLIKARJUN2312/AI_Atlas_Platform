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
    <main
      className={cn(
        "relative z-10",
        "mx-auto",
        "w-full",
        "max-w-7xl",
        "px-6",
        "py-8",
        className
      )}
    >
      {children}
    </main>
  );
}