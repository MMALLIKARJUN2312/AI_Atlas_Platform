"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import toast from "react-hot-toast";
import { ArrowLeft, Pencil, Plus } from "lucide-react";

import { AdminGuard } from "@/components/admin/admin-guard";
import { Pagination } from "@/components/company";
import { Button, Card, EmptyState, Input, LoadingSkeleton } from "@/components/ui";
import { useCompanies } from "@/hooks/use-companies";
import { useSaveCompany } from "@/hooks/use-admin";
import type { Company } from "@/types/company";
import type { CompanyWrite } from "@/types/admin";
import { CompanyForm } from "./company-form";

type Mode = { type: "list" } | { type: "create" } | { type: "edit"; company: Company };

const PAGE_SIZE = 10;

export function CompanyManagementPage() {
  return (
    <AdminGuard>
      <CompanyManagementWorkspace />
    </AdminGuard>
  );
}

function CompanyManagementWorkspace() {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [mode, setMode] = useState<Mode>({ type: "list" });
  const companies = useCompanies({ search });
  const saveCompany = useSaveCompany();

  const results = useMemo(() => companies.data ?? [], [companies.data]);
  const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE));
  const currentPage = Math.min(page, totalPages);
  const paginated = useMemo(
    () => results.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE),
    [results, currentPage],
  );

  const handleSubmit = (values: CompanyWrite) => {
    const id = mode.type === "edit" ? mode.company.id : undefined;
    saveCompany.mutate(
      { id, company: values },
      {
        onSuccess: () => {
          toast.success(mode.type === "edit" ? "Company updated" : "Company added");
          setMode({ type: "list" });
        },
        onError: () => {
          toast.error("Could not save the company. Check the fields and try again.");
        },
      }
    );
  };

  return (
    <div className="mx-auto max-w-5xl space-y-8">
      <div>
        <Link href="/admin" className="flex items-center gap-1.5 text-sm text-zinc-400 hover:text-cyan-300">
          <ArrowLeft className="h-3.5 w-3.5" />
          Back to admin
        </Link>
        <h1 className="mt-2 text-3xl font-semibold text-white">Data management</h1>
        <p className="mt-2 text-zinc-400">Manually add a company or edit an existing one. Changes appear in the directory and Ask AI immediately.</p>
      </div>

      {mode.type !== "list" ? (
        <Card className="hover:translate-y-0">
          <h2 className="mb-6 text-lg font-semibold text-white">{mode.type === "edit" ? `Edit ${mode.company.vendor_name}` : "Add a company"}</h2>
          <CompanyForm
            company={mode.type === "edit" ? mode.company : undefined}
            onSubmit={handleSubmit}
            onCancel={() => setMode({ type: "list" })}
            isSubmitting={saveCompany.isPending}
          />
        </Card>
      ) : (
        <>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <Input
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search companies..."
              aria-label="Search companies"
              className="h-11 sm:max-w-xs"
            />
            <Button onClick={() => setMode({ type: "create" })}>
              <Plus className="h-4 w-4" />
              Add company
            </Button>
          </div>

          {companies.isLoading ? (
            <div className="space-y-3" aria-busy="true" aria-label="Loading companies">
              {Array.from({ length: 6 }).map((_, index) => (
                <LoadingSkeleton key={index} className="h-16 w-full" />
              ))}
            </div>
          ) : companies.isError ? (
            <EmptyState title="Could not load companies" description="Something went wrong fetching the directory. Try refreshing the page." />
          ) : results.length ? (
            <>
              <p className="text-sm text-zinc-500">
                {results.length} {results.length === 1 ? "company" : "companies"}
                {search ? ` matching "${search}"` : ""}
              </p>

              <Card className="hover:translate-y-0">
                <div className="divide-y divide-white/5">
                  {paginated.map((company) => (
                    <div key={company.id} className="flex items-center justify-between gap-4 py-4 first:pt-0 last:pb-0">
                      <div className="min-w-0">
                        <p className="truncate font-medium text-white">{company.vendor_name}</p>
                        <p className="truncate text-sm text-zinc-400">{company.ai_category} · {company.country} · {company.company_type}</p>
                      </div>
                      <Button
                        variant="secondary"
                        onClick={() => setMode({ type: "edit", company })}
                        className="shrink-0"
                      >
                        <Pencil className="h-3.5 w-3.5" />
                        Edit
                      </Button>
                    </div>
                  ))}
                </div>
              </Card>

              <Pagination page={currentPage} totalPages={totalPages} onPageChange={setPage} />
            </>
          ) : (
            <EmptyState title="No companies found" description="Try a different search, or add a new company." />
          )}
        </>
      )}
    </div>
  );
}
