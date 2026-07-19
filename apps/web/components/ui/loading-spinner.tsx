import { cn } from "@/lib/utils";

type SpinnerSize =
  | "sm"
  | "md"
  | "lg";

export interface LoadingSpinnerProps {
  size?: SpinnerSize;
  className?: string;
}

const sizes = {
  sm: "h-4 w-4 border-2",

  md: "h-6 w-6 border-[3px]",

  lg: "h-10 w-10 border-4",
};

export function LoadingSpinner({
  size = "md",
  className,
}: LoadingSpinnerProps) {
  return (
    <span
      role="status"
      aria-label="Loading"
      className={cn(
        "inline-block animate-spin rounded-full",
        "border-white/20 border-t-cyan-400",
        sizes[size],
        className
      )}
    />
  );
}