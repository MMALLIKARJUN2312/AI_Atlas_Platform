export const API_ROUTES = {
  companies: "/companies",
  company: (companyId: number | string) => `/companies/${companyId}`,
  companyProblems: (companyId: number | string) =>
    `/companies/${companyId}/problems`,

  sectors: "/sectors",

  askAI: "/ask",

  companyNews: (companyId: number | string) =>
    `/companies/${companyId}/news`,
} as const;