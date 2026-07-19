import { useQuery } from "@tanstack/react-query";

import { problemService } from "@/services";
import { queryKeys } from "@/lib/query-keys";

interface UseProblemsOptions {
  enabled?: boolean;
}

export function useProblems(
  companyId: number | string,
  options?: UseProblemsOptions
) {
  return useQuery({
    queryKey: queryKeys.problems(companyId),

    queryFn: () =>
      problemService.getProblems(companyId),

enabled:
  options?.enabled ??
  Boolean(companyId),

    staleTime: 1000 * 60 * 5,
    gcTime: 1000 * 60 * 10,

    retry: 1,
  });
}