import { useQuery } from "@tanstack/react-query";

import { queryKeys } from "@/lib/query-keys";
import { companyService } from "@/services";

interface UseCompanyOptions {
  enabled?: boolean;
}

export function useCompany(
  companyId: number | string,
  options?: UseCompanyOptions
) {
  return useQuery({
    queryKey: queryKeys.company(companyId),

    queryFn: () =>
      companyService.getCompany(companyId),

   enabled:
  options?.enabled ??
  Boolean(companyId),

    staleTime: 1000 * 60 * 5,
    gcTime: 1000 * 60 * 10,

    retry: 1,
  });
}