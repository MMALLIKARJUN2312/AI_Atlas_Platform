import {apiClient} from "@/lib/api-client";
import { Company } from "@/types/company";

class CompanyService {
  async getCompanies() {
    const { data } = await apiClient.get<Company[]>("/companies");

    return data;
  }

  async getCompany(companyId: number | string) {
    const { data } = await apiClient.get<Company>(
      `/companies/${companyId}`
    );

    return data;
  }
}

export const companyService = new CompanyService();