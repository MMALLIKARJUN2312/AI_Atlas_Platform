import { cn } from "@/lib/utils";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({
  children,
  className,
}: CardProps) {
  return (
    <div
      className={cn(
        `
        glass

        rounded-xl

        border

        border-white/5

        bg-white/[0.03]

        p-6

        transition-all

        duration-300

        hover:border-white/10
        `,
        className
      )}
    >
      {children}
    </div>
  );
}
