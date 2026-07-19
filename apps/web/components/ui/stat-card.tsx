import { ReactNode } from "react";

import { cn } from "@/lib/utils";
import { Card } from "./card";

export interface StatCardProps {
  title: string;
  value: ReactNode;
  subtitle?: string;
  icon?: ReactNode;
  trend?: ReactNode;
  className?: string;
}

export function StatCard({
  title,
  value,
  subtitle,
  icon,
  trend,
  className,
}: StatCardProps) {
  return (
    <Card
      className={cn(
        "flex min-h-[170px] flex-col justify-between",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-400">
            {title}
          </p>

          <div className="mt-3 text-4xl font-bold tracking-tight text-white">
            {value}
          </div>
        </div>

        {icon && (
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-300">
            {icon}
          </div>
        )}
      </div>

      <div className="mt-6 flex items-center justify-between">
        {subtitle ? (
          <span className="text-sm text-zinc-500">
            {subtitle}
          </span>
        ) : (
          <span />
        )}

        {trend}
      </div>
    </Card>
  );
}