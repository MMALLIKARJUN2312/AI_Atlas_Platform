"use client";

import { useState } from "react";
import Link from "next/link";
import toast from "react-hot-toast";
import { ArrowLeft, Pencil, Plus } from "lucide-react";

import { AdminGuard } from "@/components/admin/admin-guard";
import { Card, EmptyState, Input, LoadingSkeleton } from "@/components/ui";
import { useCompanies } from "@/hooks/use-companies";
import { useSaveCompany } from "@/hooks/use-admin";
import type { Company } from "@/types/company";
import type { CompanyWrite } from "@/types/admin";
import { CompanyForm } from "./company-form";

type Mode = { type: "list" } | { type: "create" } | { type: "edit"; company: Company };

export function CompanyManagementPage() {
  return (
    <AdminGuard>
      <CompanyManagementWorkspace />
    </AdminGuard>
  );
}

function CompanyManagementWorkspace() {
  const [search, setSearch] = useState("");
  const [mode, setMode] = useState<Mode>({ type: "list" });
  const companies = useCompanies({ search });
  const saveCompany = useSaveCompany();

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
      <div className="flex items-center justify-between gap-4">
        <div>
          <Link href="/admin" className="flex items-center gap-1.5 text-sm text-zinc-400 hover:text-cyan-300">
            <ArrowLeft className="h-3.5 w-3.5" />
            Back to admin
          </Link>
          <h1 className="mt-2 text-3xl font-semibold text-white">Data management</h1>
          <p className="mt-2 text-zinc-400">Manually add a company or edit an existing one. Changes appear in the directory and Ask AI immediately.</p>
        </div>
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
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search companies..."
              className="h-11 sm:max-w-xs"
            />
            <button
              onClick={() => setMode({ type: "create" })}
              className="flex items-center justify-center gap-2 rounded-xl bg-sky-400 px-4 py-2.5 font-medium text-slate-950 transition hover:bg-sky-300"
            >
              <Plus className="h-4 w-4" />
              Add company
            </button>
          </div>

          {companies.isLoading ? (
            <div className="space-y-3">
              {Array.from({ length: 5 }).map((_, index) => (
                <LoadingSkeleton key={index} className="h-16 w-full" />
              ))}
            </div>
          ) : companies.isError ? (
            <EmptyState title="Could not load companies" description="Something went wrong fetching the directory. Try refreshing the page." />
          ) : companies.data?.length ? (
            <Card className="hover:translate-y-0">
              <div className="divide-y divide-white/5">
                {companies.data.map((company) => (
                  <div key={company.id} className="flex items-center justify-between gap-4 py-4 first:pt-0 last:pb-0">
                    <div className="min-w-0">
                      <p className="truncate font-medium text-white">{company.vendor_name}</p>
                      <p className="truncate text-sm text-zinc-400">{company.ai_category} · {company.country} · {company.company_type}</p>
                    </div>
                    <button
                      onClick={() => setMode({ type: "edit", company })}
                      className="flex shrink-0 items-center gap-1.5 rounded-xl border border-white/10 px-3 py-2 text-sm text-zinc-300 hover:border-cyan-400/40 hover:text-cyan-300"
                    >
                      <Pencil className="h-3.5 w-3.5" />
                      Edit
                    </button>
                  </div>
                ))}
              </div>
            </Card>
          ) : (
            <EmptyState title="No companies found" description="Try a different search, or add a new company." />
          )}
        </>
      )}
    </div>
  );
}
