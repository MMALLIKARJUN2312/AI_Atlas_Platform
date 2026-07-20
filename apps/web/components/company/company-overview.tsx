import {
  BrainCircuit,
  FileText,
  Users,
} from "lucide-react";

import { Card } from "@/components/ui";
import { Company } from "@/types/company";

interface CompanyOverviewProps {
  company: Company;
}

function Section({
  icon: Icon,
  title,
  content,
}: {
  icon: React.ElementType;
  title: string;
  content?: string | null;
}) {
  return (
    <div className="rounded-lg border border-white/10 bg-zinc-950/50 p-5">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600/10">
          <Icon
            size={18}
            className="text-blue-500"
          />
        </div>

        <h3 className="text-lg font-semibold text-white">
          {title}
        </h3>
      </div>

      <p className="mt-4 whitespace-pre-line text-sm leading-6 text-zinc-300">
        {content || "No information available."}
      </p>
    </div>
  );
}

export function CompanyOverview({
  company,
}: CompanyOverviewProps) {
  return (
    <Card className="border border-zinc-800 bg-zinc-900">
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white">
          Company Overview
        </h2>

        <p className="mt-1 text-sm text-zinc-400">
          AI adoption, deployment evidence and customer landscape.
        </p>
      </div>

      <div className="space-y-4">
        <Section
          icon={BrainCircuit}
          title="AI Use Case"
          content={company.food_beverage_ai_use_case}
        />

        <Section
          icon={FileText}
          title="Deployment Evidence"
          content={company.top_deployment_evidence}
        />

        <Section
          icon={Users}
          title="Major Customers"
          content={
            company.top_germany_food_beverage_customers
          }
        />
      </div>
    </Card>
  );
}
