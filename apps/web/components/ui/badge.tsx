import { cn } from "@/lib/utils";

interface BadgeProps {
  children: React.ReactNode;
  className?: string;
}

export function Badge({
  children,
  className,
}: BadgeProps) {
  return (
    <span
      className={cn(
        `
        inline-flex
        items-center
        rounded-full
        border
        border-cyan-400/30
        bg-cyan-500/10
        px-4
        py-1.5
        text-sm
        font-medium
        text-cyan-300
        backdrop-blur-xl
        `,
        className
      )}
    >
      {children}
    </span>
  );
}