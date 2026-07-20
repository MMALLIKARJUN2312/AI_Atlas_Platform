import { apiClient } from "@/lib/api-client";
import type { Company } from "@/types/company";
import type { CompanyCandidate, CompanyWrite } from "@/types/admin";

class AdminService {
  async discover(sector: string, country: string) { return (await apiClient.post<CompanyCandidate[]>("/admin/discover", { sector, country })).data; }
  async candidates() { return (await apiClient.get<CompanyCandidate[]>("/admin/candidates")).data; }
  async approve(id: number) { return (await apiClient.post<Company>(`/admin/candidates/${id}/approve`)).data; }
  async reject(id: number) { return (await apiClient.post<CompanyCandidate>(`/admin/candidates/${id}/reject`)).data; }
  async createCompany(company: CompanyWrite) { return (await apiClient.post<Company>("/admin/companies", company)).data; }
  async updateCompany(id: number, company: CompanyWrite) { return (await apiClient.put<Company>(`/admin/companies/${id}`, company)).data; }
}
export const adminService = new AdminService();
