"use client";

import { useMemo } from "react";
import Link from "next/link";
import {
  ArrowRight,
  Boxes,
  Brain,
  Building2,
  Database,
  Search,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { Button, Card, EmptyState, LoadingSkeleton, StatCard } from "@/components/ui";
import { useCompanies, useSectors } from "@/hooks";

export function DashboardPage() {
  const { data: companies = [], isLoading: companiesLoading, isError: companiesError } = useCompanies({});
  const { data: sectors = [], isLoading: sectorsLoading } = useSectors();

  const aiCategoryCount = useMemo(
    () => new Set(companies.map((company) => company.ai_category)).size,
    [companies],
  );

  const maturityLevelCount = useMemo(
    () => new Set(companies.map((company) => company.maturity)).size,
    [companies],
  );

  const recentCompanies = useMemo(
    () => [...companies].sort((a, b) => b.id - a.id).slice(0, 5),
    [companies],
  );

  const isLoading = companiesLoading || sectorsLoading;

  return (
    <div className="space-y-8">
      <section className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="flex items-center gap-2 text-sm font-medium text-cyan-300">
            <Sparkles className="h-4 w-4" />
            Welcome to AI Atlas
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Germany&apos;s Food &amp; Beverage AI intelligence, in one place
          </h1>
          <p className="mt-3 max-w-2xl text-zinc-400">
            Browse verified AI vendors, ask grounded questions with citations, and stay current with
            automated company news — all backed by a curated, continuously indexed knowledge base.
          </p>
        </div>

        <div className="flex shrink-0 flex-wrap gap-3">
          <Button asChild>
            <Link href="/ask-ai">
              <Brain className="h-4 w-4" />
              Ask AI
            </Link>
          </Button>
          <Link
            href="/companies"
            className="flex items-center gap-2 rounded-lg border border-white/10 px-4 py-2.5 text-sm font-medium text-zinc-300 transition hover:border-cyan-400/40 hover:text-cyan-300"
          >
            <Search className="h-4 w-4" />
            Browse companies
          </Link>
        </div>
      </section>

      {companiesError ? (
        <EmptyState
          title="Dashboard data could not be loaded"
          description="Please check that the API is running, then refresh the page."
        />
      ) : isLoading ? (
        <DashboardSkeleton />
      ) : (
        <>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard title="Companies" value={companies.length} icon={<Building2 className="h-5 w-5" />} subtitle="Indexed AI vendors" />
            <StatCard title="Sectors" value={sectors.length} icon={<Boxes className="h-5 w-5" />} subtitle="F&B industry segments" />
            <StatCard title="AI categories" value={aiCategoryCount} icon={<Sparkles className="h-5 w-5" />} subtitle="Distinct AI category tags" />
            <StatCard title="Maturity levels" value={maturityLevelCount} icon={<ShieldCheck className="h-5 w-5" />} subtitle="From pilot to commodity" />
          </section>

          <section className="grid gap-6 lg:grid-cols-3">
            <Card className="hover:translate-y-0 lg:col-span-2">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-white">Recently added companies</h2>
                <Link href="/companies" className="flex items-center gap-1 text-sm text-cyan-300 hover:text-cyan-200">
                  View all
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>

              {recentCompanies.length === 0 ? (
                <p className="mt-6 text-sm text-zinc-400">No companies indexed yet.</p>
              ) : (
                <ul className="mt-5 divide-y divide-white/5">
                  {recentCompanies.map((company) => (
                    <li key={company.id}>
                      <Link
                        href={`/companies/${company.id}`}
                        className="flex items-center justify-between gap-4 py-3.5 first:pt-0 last:pb-0"
                      >
                        <div className="min-w-0">
                          <p className="truncate font-medium text-white">{company.vendor_name}</p>
                          <p className="truncate text-sm text-zinc-400">{company.ai_category} · {company.country}</p>
                        </div>
                        <ArrowRight className="h-4 w-4 shrink-0 text-zinc-500" />
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </Card>

            <Card className="hover:translate-y-0">
              <h2 className="text-lg font-semibold text-white">Admin workspace</h2>
              <p className="mt-2 text-sm text-zinc-400">
                Discover new vendors, review evidence, and manage the directory.
              </p>

              <div className="mt-5 space-y-2">
                <Link
                  href="/admin"
                  className="flex items-center justify-between rounded-xl border border-white/10 px-4 py-3 text-sm text-zinc-300 transition hover:border-cyan-400/40 hover:text-cyan-300"
                >
                  <span className="flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4" />
                    Company discovery
                  </span>
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <Link
                  href="/admin/companies"
                  className="flex items-center justify-between rounded-xl border border-white/10 px-4 py-3 text-sm text-zinc-300 transition hover:border-cyan-400/40 hover:text-cyan-300"
                >
                  <span className="flex items-center gap-2">
                    <Database className="h-4 w-4" />
                    Data management
                  </span>
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </Card>
          </section>
        </>
      )}
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-8" aria-busy="true" aria-label="Loading dashboard">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[...Array(4)].map((_, index) => (
          <LoadingSkeleton key={index} className="h-[170px]" />
        ))}
      </div>
      <div className="grid gap-6 lg:grid-cols-3">
        <LoadingSkeleton className="h-72 lg:col-span-2" />
        <LoadingSkeleton className="h-72" />
      </div>
    </div>
  );
}
