import {
  ButtonHTMLAttributes,
  forwardRef,
} from "react";

import { cn } from "@/lib/utils";
import { LoadingSpinner } from "./loading-spinner";

type ButtonVariant =
  | "primary"
  | "secondary"
  | "ghost"
  | "danger";

type ButtonSize =
  | "sm"
  | "md"
  | "lg";

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
}

const variantClasses = {
  primary:
    "bg-cyan-500 text-white hover:bg-cyan-400",

  secondary:
    "border border-white/10 bg-white/5 text-white hover:bg-white/10",

  ghost:
    "bg-transparent text-zinc-300 hover:bg-white/5",

  danger:
    "bg-red-600 text-white hover:bg-red-500",
};

const sizeClasses = {
  sm: "h-9 px-4 text-sm",

  md: "h-11 px-5 text-sm",

  lg: "h-12 px-6 text-base",
};

export const Button = forwardRef<
  HTMLButtonElement,
  ButtonProps
>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      loading = false,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          "inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-all duration-200",
          "focus:outline-none focus:ring-2 focus:ring-cyan-400",
          "disabled:cursor-not-allowed disabled:opacity-50",
          variantClasses[variant],
          sizeClasses[size],
          className
        )}
        {...props}
      >
        {loading && (
  <LoadingSpinner size="sm" />
)}

        {children}
      </button>
    );
  }
);

Button.displayName = "Button";