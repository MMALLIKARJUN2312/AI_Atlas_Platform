import { Building2, ExternalLink, Globe } from "lucide-react";

import { Badge, Button, Card } from "@/components/ui";
import { Company } from "@/types/company";

interface CompanyHeaderProps {
  company: Company;
}

export function CompanyHeader({
  company,
}: CompanyHeaderProps) {
  return (
    <Card className="border border-zinc-800 bg-zinc-900">
      <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
        <div className="flex gap-5">
          <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-blue-600/10">
            <Building2
              size={30}
              className="text-blue-500"
            />
          </div>

          <div className="space-y-4">
            <div className="flex flex-wrap items-center gap-3">
              <h1 className="text-3xl font-semibold text-white">
                {company.vendor_name}
              </h1>

              <Badge>
                {company.maturity}
              </Badge>
            </div>

            <p className="max-w-3xl text-zinc-400">
              {company.ai_category}
            </p>

            <div className="flex flex-wrap items-center gap-6 text-sm text-zinc-400">
              <div className="flex items-center gap-2">
                <Globe size={16} />
                <span>{company.country}</span>
              </div>

              <div>
                {company.company_type}
              </div>

              <div>
                {company.funding}
              </div>
            </div>
          </div>
        </div>

        <Button asChild>
          <a
            href={company.website}
            target="_blank"
            rel="noopener noreferrer"
          >
            Visit Website
            <ExternalLink size={16} />
          </a>
        </Button>
      </div>
    </Card>
  );
}