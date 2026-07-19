import { useQuery } from "@tanstack/react-query";

import { sectorService } from "@/services";
import { queryKeys } from "@/lib/query-keys";

export function useSectors() {
  return useQuery({
    queryKey: queryKeys.sectors,

    queryFn: () =>
      sectorService.getSectors(),

    staleTime: 1000 * 60 * 30,
    gcTime: 1000 * 60 * 60,

    retry: 1,
    refetchOnWindowFocus: false,
  });
}