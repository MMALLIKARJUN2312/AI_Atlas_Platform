import { cn } from "@/lib/utils";

interface GlassPanelProps {
  children: React.ReactNode;
  className?: string;
}

export function GlassPanel({
  children,
  className,
}: GlassPanelProps) {
  return (
    <section
      className={cn(
        `
        glass
        rounded-[36px]
        border
        border-white/5
        bg-white/[0.02]
        p-8
        backdrop-blur-3xl
        `,
        className
      )}
    >
      {children}
    </section>
  );
}