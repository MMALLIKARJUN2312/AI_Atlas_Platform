import { cn } from "@/lib/utils";

interface SurfaceProps {
  children: React.ReactNode;
  className?: string;
}

export function Surface({
  children,
  className,
}: SurfaceProps) {
  return (
    <div
      className={cn(
        "glass rounded-[32px]",
        className
      )}
    >
      {children}
    </div>
  );
}