"use client";

import toast from "react-hot-toast";
import { ExternalLink, RefreshCw, Rss } from "lucide-react";

import { Button, EmptyState, LoadingSkeleton } from "@/components/ui";
import { useCompanyNews, useRefreshCompanyNews } from "@/hooks";

interface CompanyNewsProps {
  companyId: number;
}

export function CompanyNews({ companyId }: CompanyNewsProps) {
  const { data, isLoading, isError } = useCompanyNews(companyId);
  const refreshNews = useRefreshCompanyNews(companyId);
  const handleRefresh = () =>
    refreshNews.mutate(undefined, {
      onSuccess: (result) => {
        toast.success(
          result.added_count > 0
            ? `Found ${result.added_count} new article${result.added_count === 1 ? "" : "s"}`
            : "No new articles found",
        );
      },
      onError: () => toast.error("News refresh failed. Please try again."),
    });

  if (isLoading) {
    return <CompanyNewsSkeleton />;
  }

  if (isError) {
    return (
      <EmptyState
        title="News could not be loaded"
        description="Please try refreshing the company news."
        action={<RefreshButton isRefreshing={refreshNews.isPending} onClick={handleRefresh} />}
      />
    );
  }

  if (!data?.articles.length) {
    return (
      <EmptyState
        icon={<Rss size={28} />}
        title="No recent news found"
        description="News automation will populate this section when relevant coverage is available."
        action={<RefreshButton isRefreshing={refreshNews.isPending} onClick={handleRefresh} />}
      />
    );
  }

  return (
    <section className="space-y-5" aria-label="Company news">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-white">Newsletter</h2>
          <p className="mt-1 text-sm text-zinc-400">
            Relevant company coverage from public sources.
          </p>
        </div>
        <RefreshButton isRefreshing={refreshNews.isPending} onClick={handleRefresh} />
      </div>

      <div className="space-y-4">
        {data.articles.map((article) => (
          <article key={article.id} className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-sm text-cyan-300">
                  {article.source_name} · {new Date(article.published_at).toLocaleDateString()}
                </p>
                <h3 className="mt-2 text-lg font-semibold text-white">{article.title}</h3>
              </div>
              <a
                href={article.source_url}
                target="_blank"
                rel="noreferrer"
                aria-label={`Open article: ${article.title}`}
                className="inline-flex items-center gap-2 text-sm text-cyan-300 hover:text-cyan-200"
              >
                Read article <ExternalLink size={16} />
              </a>
            </div>
            <p className="mt-4 leading-7 text-zinc-300">
              {article.summary || "No summary available."}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}

function RefreshButton({ isRefreshing, onClick }: { isRefreshing: boolean; onClick: () => void }) {
  return (
    <Button type="button" onClick={onClick} disabled={isRefreshing}>
      <RefreshCw className={isRefreshing ? "animate-spin" : ""} size={16} />
      {isRefreshing ? "Refreshing…" : "Refresh News"}
    </Button>
  );
}

function CompanyNewsSkeleton() {
  return (
    <div className="space-y-4" aria-busy="true" aria-label="Loading company news">
      <LoadingSkeleton className="h-16 w-1/3" />
      <LoadingSkeleton className="h-44 w-full" />
      <LoadingSkeleton className="h-44 w-full" />
    </div>
  );
}
