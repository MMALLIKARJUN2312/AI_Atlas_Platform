import { apiClient } from "@/lib/api-client";
import type { CompanyNewsResponse, NewsRefreshResponse } from "@/types/news";

class NewsService {
  async getCompanyNews(companyId: number | string) {
    const { data } = await apiClient.get<CompanyNewsResponse>(`/companies/${companyId}/news`);
    return data;
  }

  async refreshCompanyNews(companyId: number | string) {
    const { data } = await apiClient.post<NewsRefreshResponse>(
      `/companies/${companyId}/news/refresh`,
    );
    return data;
  }
}

export const newsService = new NewsService();
