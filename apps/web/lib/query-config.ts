export const DEFAULT_QUERY_OPTIONS = {
  staleTime: 1000 * 60 * 5,
  gcTime: 1000 * 60 * 10,
  retry: 1,
  refetchOnWindowFocus: false,
} as const;