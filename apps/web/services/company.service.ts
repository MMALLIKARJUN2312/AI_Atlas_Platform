import { apiClient } from "@/lib/api-client";
import { Company, CompanyFilters } from "@/types/company";

class CompanyService {
  async getCompanies(filters: CompanyFilters = {}) {
    const { data } = await apiClient.get<Company[]>("/companies", {
      params: {
        search: filters.search || undefined,
        segment: filters.segment || undefined,
        company_type: filters.companyType || undefined,
        maturity: filters.maturity || undefined,
        ai_category: filters.aiCategory || undefined,
      },
    });

    return data;
  }

  async getCompany(companyId: number | string) {
    const { data } = await apiClient.get<Company>(`/companies/${companyId}`);

    return data;
  }
}

export const companyService = new CompanyService();
