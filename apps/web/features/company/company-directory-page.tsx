"use client";

import { useMemo, useState } from "react";
import { Building2, Boxes, BrainCircuit, Star } from "lucide-react";

import { CompanyGrid, CompanySearch, SectorFilter } from "@/components/company";

import { EmptyState, GlassPanel, LoadingSkeleton } from "@/components/ui";

import { useCompanies, useSectors } from "@/hooks";

function StatCard({
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

  const {
    data: companies = [],
    isLoading: companiesLoading,
    isError: companiesError,
  } = useCompanies();

  const { data: sectors = [], isError: sectorsError } = useSectors();

  const companyTypes = useMemo(
    () => Array.from(new Set(companies.map((company) => company.company_type))).sort(),
    [companies],
  );

  const [companyType, setCompanyType] = useState("");

  const filteredCompanies = useMemo(() => {
    return companies.filter((c) => {
      const matchesSearch =
        c.vendor_name.toLowerCase().includes(search.toLowerCase()) ||
        c.ai_category.toLowerCase().includes(search.toLowerCase());

      const matchesSector = !sector || c.segment_tags.includes(sector);

      const matchesCompanyType = !companyType || c.company_type === companyType;

      return matchesSearch && matchesSector && matchesCompanyType;
    });
  }, [companies, search, sector, companyType]);

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
    <div className="space-y-12">
      {/* Hero */}

      <section className="grid grid-cols-12 gap-8">
        <div className="col-span-8">
          <h1 className="text-6xl font-black leading-tight">
            Discover{" "}
            <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 bg-clip-text text-transparent">
              AI Companies
            </span>
          </h1>

          <p className="mt-5 max-w-3xl text-xl text-slate-400">
            Explore Germany&apos;s Food & Beverage AI ecosystem.
          </p>

          <div className="mt-10">
            <CompanySearch value={search} total={companies.length} onChange={setSearch} />
          </div>
        </div>

        <div className="col-span-4 grid grid-cols-2 gap-5">
          <StatCard icon={Building2} label="Companies" value={companies.length} />

          <StatCard icon={Boxes} label="Sectors" value={sectors.length} />

          <StatCard icon={BrainCircuit} label="AI Use Cases" value="356" />

          <StatCard icon={Star} label="Maturity" value="4" />
        </div>
      </section>

      {/* Filters */}

      <section className="space-y-6">
        {sectorsError ? (
          <p className="text-sm text-amber-300">Sector filters are temporarily unavailable.</p>
        ) : (
          <SectorFilter sectors={sectors} selectedSector={sector} onSelect={setSector} />
        )}

        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-slate-400">Showing {filteredCompanies.length} companies</p>

          <select
            value={companyType}
            onChange={(event) => setCompanyType(event.target.value)}
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
        </div>
      </section>

      {/* Grid */}

      {filteredCompanies.length === 0 ? (
        <EmptyState title="No Companies" description="Try changing the search or filters." />
      ) : (
        <CompanyGrid companies={filteredCompanies} />
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
