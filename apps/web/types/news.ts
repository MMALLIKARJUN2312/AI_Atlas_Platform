export interface NewsArticle {
  id: number;
  title: string;
  summary: string;
  source_name: string;
  source_url: string;
  published_at: string;
}

export interface CompanyNewsResponse {
  articles: NewsArticle[];
}

export interface NewsRefreshResponse extends CompanyNewsResponse {
  added_count: number;
}
