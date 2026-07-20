"use client";

import { type ReactNode, use, useState } from "react";

import {
  CompanyDetailsGrid,
  CompanyHeader,
  CompanyOverview,
  CompanyTags,
} from "@/components/company";
import { Card, EmptyState, LoadingSkeleton } from "@/components/ui";
import { useCompany, useProblems } from "@/hooks";

interface CompanyDetailPageProps {
  params: Promise<{
    companyId: string;
  }>;
}

export function CompanyDetailPage({ params }: CompanyDetailPageProps) {
  const { companyId } = use(params);
  const [activeTab, setActiveTab] = useState<"overview" | "problems">("overview");

  const { data: company, isLoading: companyLoading, isError: companyError } = useCompany(companyId);

  const {
    data: problems = [],
    isLoading: problemsLoading,
    isError: problemsError,
  } = useProblems(companyId);

  if (companyLoading) {
    return <CompanyDetailSkeleton />;
  }

  if (companyError || !company) {
    return (
      <EmptyState
        title="Company not found"
        description="The requested company could not be loaded."
      />
    );
  }

  return (
    <div className="space-y-10">
      <CompanyHeader company={company} />

      <CompanyTags tags={company.segment_tags} />

      <div
        className="flex gap-2 border-b border-zinc-800"
        role="tablist"
        aria-label="Company profile sections"
      >
        <ProfileTab active={activeTab === "overview"} onClick={() => setActiveTab("overview")}>
          Overview
        </ProfileTab>
        <ProfileTab active={activeTab === "problems"} onClick={() => setActiveTab("problems")}>
          Problems Solved
        </ProfileTab>
        <ProfileTab active={false} disabled>
          Newsletter
        </ProfileTab>
      </div>

      {activeTab === "overview" ? (
        <div className="grid gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <CompanyOverview company={company} />
          </div>
          <CompanyDetailsGrid company={company} />
        </div>
      ) : (
        <Card>
          <h2 className="mb-6 text-2xl font-semibold text-white">AI Problems Solved</h2>

          {problemsLoading ? (
            <div className="space-y-4" aria-busy="true">
              <LoadingSkeleton className="h-36 w-full" />
              <LoadingSkeleton className="h-36 w-full" />
            </div>
          ) : problemsError ? (
            <EmptyState
              title="Problems could not be loaded"
              description="Please refresh the page to try again."
            />
          ) : problems.length === 0 ? (
            <EmptyState
              title="No Problems Available"
              description="No mapped problems were found for this company."
            />
          ) : (
            <div className="space-y-6">
              {problems.map((problem) => (
                <div key={problem.problem_id} className="rounded-xl border border-zinc-800 p-6">
                  <h3 className="text-lg font-semibold text-white">{problem.problem_statement}</h3>

                  <p className="mt-3 text-zinc-400">{problem.ai_use_case_solution}</p>

                  <div className="mt-5 flex flex-wrap gap-2">
                    <span className="rounded-full bg-zinc-800 px-3 py-1 text-sm text-zinc-300">
                      {problem.category}
                    </span>

                    <span className="rounded-full bg-zinc-800 px-3 py-1 text-sm text-zinc-300">
                      {problem.severity}
                    </span>

                    <span className="rounded-full bg-zinc-800 px-3 py-1 text-sm text-zinc-300">
                      ROI: {problem.roi_benchmark}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}
    </div>
  );
}

function ProfileTab({
  active,
  children,
  disabled,
  onClick,
}: {
  active: boolean;
  children: ReactNode;
  disabled?: boolean;
  onClick?: () => void;
}) {
  return (
    <button
      type="button"
      role="tab"
      aria-selected={active}
      disabled={disabled}
      onClick={onClick}
      className={`border-b-2 px-4 py-3 text-sm font-medium transition ${active ? "border-cyan-400 text-cyan-300" : "border-transparent text-zinc-400 hover:text-white"} disabled:cursor-not-allowed disabled:opacity-50`}
    >
      {children}
    </button>
  );
}

function CompanyDetailSkeleton() {
  return (
    <div className="space-y-10" aria-busy="true" aria-label="Loading company profile">
      <LoadingSkeleton className="h-48 w-full" />
      <LoadingSkeleton className="h-8 w-2/3" />
      <div className="grid gap-8 lg:grid-cols-3">
        <LoadingSkeleton className="h-[32rem] lg:col-span-2" />
        <LoadingSkeleton className="h-[32rem]" />
      </div>
    </div>
  );
}
