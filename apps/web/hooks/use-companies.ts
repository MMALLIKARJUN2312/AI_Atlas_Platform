import { useQuery } from "@tanstack/react-query";

import { companyService } from "@/services";
import { queryKeys } from "@/lib/query-keys";

export function useCompanies() {
  return useQuery({
    queryKey: queryKeys.companies,
    queryFn: () => companyService.getCompanies(),

    staleTime: 1000 * 60 * 5,
    gcTime: 1000 * 60 * 10,

    refetchOnWindowFocus: false,
    retry: 1,
  });
}