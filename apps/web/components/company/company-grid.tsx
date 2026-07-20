import { Company } from "@/types/company";
import { CompanyCard } from "./company-card";

interface Props {
  companies: Company[];
}

export function CompanyGrid({
  companies,
}: Props) {
  return (
    <div
      className="
        grid
        gap-6
        xl:grid-cols-2
      "
    >
      {companies.map((company) => (
        <CompanyCard
          key={company.id}
          company={company}
        />
      ))}
    </div>
  );
}
