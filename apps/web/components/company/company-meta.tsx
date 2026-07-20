import { ReactNode } from "react";

interface CompanyMetaProps {
  label: string;
  value: ReactNode;
}

export function CompanyMeta({
  label,
  value,
}: CompanyMetaProps) {
  return (
    <div className="flex items-start justify-between gap-4 text-sm">
      <span className="text-zinc-500">
        {label}
      </span>

      <span className="text-right font-medium text-white">
        {value}
      </span>
    </div>
  );
}