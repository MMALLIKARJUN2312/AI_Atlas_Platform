"use client";

import { useMemo, useState } from "react";
import { Building2, Boxes, BrainCircuit, Layers3 } from "lucide-react";

import { CompanyGrid, CompanySearch, Pagination, SectorFilter } from "@/components/company";

import { EmptyState, GlassPanel, LoadingSkeleton } from "@/components/ui";

import { useCompanies, useSectors } from "@/hooks";
import type { CompanyFilters } from "@/types/company";

const PAGE_SIZE = 12;

function DirectoryStatCard({
  icon: Icon,
  label,
  value,
}: {
  icon: React.ElementType;
  label: string;
  value: string | number;
}) {
  return (
    <GlassPanel className="flex h-40 flex-col justify-between rounded-3xl border border-cyan-500/10 bg-white/[0.02] p-6">
      <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-500/10">
        <Icon className="text-cyan-400" size={24} />
      </div>

      <div>
        <h2 className="text-4xl font-bold">{value}</h2>

        <p className="mt-1 text-slate-400">{label}</p>
      </div>
    </GlassPanel>
  );
}

export function CompanyDirectoryPage() {
  const [search, setSearch] = useState("");
  const [sector, setSector] = useState("");
  const [companyType, setCompanyType] = useState("");
  const [maturity, setMaturity] = useState("");
  const [aiCategory, setAiCategory] = useState("");
  const [page, setPage] = useState(1);

  const filters = useMemo<CompanyFilters>(
    () => ({
      search,
      segment: sector,
      companyType,
      maturity,
      aiCategory,
    }),
    [aiCategory, companyType, maturity, search, sector],
  );
  const {
    data: companies = [],
    isLoading: companiesLoading,
    isError: companiesError,
  } = useCompanies(filters);

  // Unfiltered load, used only to build stable filter-dropdown option lists so
  // the available options don't shrink/change as the user narrows the results.
  const { data: allCompanies = [] } = useCompanies({});

  const { data: sectors = [], isError: sectorsError } = useSectors();

  const companyTypes = useMemo(
    () => Array.from(new Set(allCompanies.map((company) => company.company_type))).sort(),
    [allCompanies],
  );

  const maturities = useMemo(
    () => Array.from(new Set(allCompanies.map((company) => company.maturity))).sort(),
    [allCompanies],
  );

  const aiCategoryCount = useMemo(
    () => new Set(allCompanies.map((company) => company.ai_category)).size,
    [allCompanies],
  );

  const totalPages = Math.max(1, Math.ceil(companies.length / PAGE_SIZE));
  const currentPage = Math.min(page, totalPages);
  const paginatedCompanies = useMemo(
    () => companies.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE),
    [companies, currentPage],
  );

  if (companiesLoading) {
    return <CompanyDirectorySkeleton />;
  }

  if (companiesError) {
    return (
      <EmptyState
        title="Companies could not be loaded"
        description="Please check that the API is running, then refresh the page."
      />
    );
  }

  return (
    <div className="space-y-8">
      {/* Hero */}

      <section className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_420px]">
        <div>
          <h1 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            AI Companies
          </h1>

          <p className="mt-3 max-w-2xl text-base text-zinc-400 sm:text-lg">
            Explore Germany&apos;s Food & Beverage AI ecosystem.
          </p>

          <div className="mt-7 max-w-2xl">
            <CompanySearch
              value={search}
              total={companies.length}
              onChange={(value) => {
                setSearch(value);
                setPage(1);
              }}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <DirectoryStatCard icon={Building2} label="Companies" value={allCompanies.length} />

          <DirectoryStatCard icon={Boxes} label="Sectors" value={sectors.length} />

          <DirectoryStatCard icon={BrainCircuit} label="AI Categories" value={aiCategoryCount} />

          <DirectoryStatCard icon={Layers3} label="Maturity Levels" value={maturities.length} />
        </div>
      </section>

      {/* Filters */}

      <section className="space-y-5">
        {sectorsError ? (
          <p className="text-sm text-amber-300">Sector filters are temporarily unavailable.</p>
        ) : (
          <SectorFilter
            sectors={sectors}
            selectedSector={sector}
            onSelect={(value) => {
              setSector(value);
              setPage(1);
            }}
          />
        )}

        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-slate-400">Showing {companies.length} companies</p>

          <div className="grid gap-3 sm:grid-cols-3">
            <select
              value={companyType}
              onChange={(event) => {
                setCompanyType(event.target.value);
                setPage(1);
              }}
              aria-label="Filter by company type"
              className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm"
            >
              <option value="">All company types</option>
              {companyTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>

            <select
              value={maturity}
              onChange={(event) => {
                setMaturity(event.target.value);
                setPage(1);
              }}
              aria-label="Filter by maturity"
              className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm"
            >
              <option value="">All maturity levels</option>
              {maturities.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>

            <input
              value={aiCategory}
              onChange={(event) => {
                setAiCategory(event.target.value);
                setPage(1);
              }}
              placeholder="AI category"
              aria-label="Filter by AI category"
              className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm placeholder:text-zinc-500"
            />
          </div>
        </div>
      </section>

      {/* Grid */}

      {companies.length === 0 ? (
        <EmptyState title="No Companies" description="Try changing the search or filters." />
      ) : (
        <>
          <CompanyGrid companies={paginatedCompanies} />
          <Pagination page={currentPage} totalPages={totalPages} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}

function CompanyDirectorySkeleton() {
  return (
    <div className="space-y-12" aria-busy="true" aria-label="Loading companies">
      <div className="grid gap-8 lg:grid-cols-12">
        <div className="space-y-5 lg:col-span-8">
          <LoadingSkeleton className="h-16 w-3/4" />
          <LoadingSkeleton className="h-7 w-1/2" />
          <LoadingSkeleton className="h-12 w-full" />
        </div>
        <div className="grid grid-cols-2 gap-5 lg:col-span-4">
          {[...Array(4)].map((_, index) => (
            <LoadingSkeleton key={index} className="h-40" />
          ))}
        </div>
      </div>
      <LoadingSkeleton className="h-16 w-full" />
      <div className="grid gap-6 lg:grid-cols-2 2xl:grid-cols-3">
        {[...Array(6)].map((_, index) => (
          <LoadingSkeleton key={index} className="h-80" />
        ))}
      </div>
    </div>
  );
}
