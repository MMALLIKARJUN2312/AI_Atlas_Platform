import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { queryKeys } from "@/lib/query-keys";
import { newsService } from "@/services";

export function useCompanyNews(companyId: number | string, enabled = true) {
  return useQuery({
    queryKey: queryKeys.companyNews(companyId),
    queryFn: () => newsService.getCompanyNews(companyId),
    enabled: Boolean(companyId) && enabled,
    staleTime: 1000 * 60 * 5,
    retry: 1,
  });
}

export function useRefreshCompanyNews(companyId: number | string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => newsService.refreshCompanyNews(companyId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.companyNews(companyId) }),
  });
}
