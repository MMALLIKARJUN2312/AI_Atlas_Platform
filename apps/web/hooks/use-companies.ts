import { useQuery } from "@tanstack/react-query";

import { companyService } from "@/services";
import { queryKeys } from "@/lib/query-keys";
import type { CompanyFilters } from "@/types/company";

export function useCompanies(filters: CompanyFilters = {}) {
  return useQuery({
    queryKey: queryKeys.companies(filters),
    queryFn: () => companyService.getCompanies(filters),

    staleTime: 1000 * 60 * 5,
    gcTime: 1000 * 60 * 10,

    refetchOnWindowFocus: false,
    retry: 1,
  });
}
