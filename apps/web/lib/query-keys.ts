export const queryKeys = {
  companies: ["companies"] as const,

  company: (id: number | string) =>
    ["company", id] as const,

  problems: (companyId: number | string) =>
    ["problems", companyId] as const,

  sectors: ["sectors"] as const,
};