import {
  Building2,
  CircleDollarSign,
  Landmark,
  Sparkles,
  TrendingUp,
  MapPinned,
} from "lucide-react";

import { Card } from "@/components/ui";
import { Company } from "@/types/company";

interface CompanyDetailsGridProps {
  company: Company;
}

const items = (company: Company) => [
  {
    label: "Company Type",
    value: company.company_type,
    icon: Building2,
  },
  {
    label: "Funding",
    value: company.funding,
    icon: TrendingUp,
  },
  {
    label: "Revenue",
    value: company.estimated_revenue,
    icon: CircleDollarSign,
  },
  {
    label: "Germany Presence",
    value: company.germany_presence,
    icon: MapPinned,
  },
  {
    label: "AI Category",
    value: company.ai_category,
    icon: Sparkles,
  },
  {
    label: "Maturity",
    value: company.maturity,
    icon: Landmark,
  },
];

export function CompanyDetailsGrid({
  company,
}: CompanyDetailsGridProps) {
  return (
    <Card className="border border-zinc-800 bg-zinc-900">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">
          Company Information
        </h2>

        <p className="mt-1 text-sm text-zinc-400">
          Business profile and AI adoption details.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        {items(company).map((item) => {
          const Icon = item.icon;

          return (
            <div
              key={item.label}
              className="rounded-lg border border-white/10 bg-zinc-950/50 p-4"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600/10">
                  <Icon
                    size={18}
                    className="text-blue-500"
                  />
                </div>

                <span className="text-sm text-zinc-400">
                  {item.label}
                </span>
              </div>

              <p className="mt-3 break-words text-sm font-medium leading-6 text-white">
                {item.value || "-"}
              </p>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
