import type { CompanyFilters } from "@/types/company";

export const queryKeys = {
  companies: (filters: CompanyFilters = {}) => ["companies", filters] as const,

  company: (id: number | string) => ["company", id] as const,

  problems: (companyId: number | string) => ["problems", companyId] as const,

  sectors: ["sectors"] as const,
};
