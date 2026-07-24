"use client";

import { type FormEvent, useState } from "react";
import Link from "next/link";
import toast from "react-hot-toast";
import { Check, Database, ExternalLink, LogOut, Search, X } from "lucide-react";

import { Button, Card, EmptyState, Input, LoadingSkeleton } from "@/components/ui";
import { AdminGuard } from "@/components/admin/admin-guard";
import { useCandidates, useDiscoverCompanies, useReviewCandidate } from "@/hooks/use-admin";
import { useAuth } from "@/providers/auth-provider";

export function AdminPage() {
  return (
    <AdminGuard>
      <AdminWorkspace />
    </AdminGuard>
  );
}

function AdminWorkspace() {
  const [sector, setSector] = useState("Dairy Processing");
  const [country, setCountry] = useState("Germany");
  const candidates = useCandidates();
  const discover = useDiscoverCompanies();
  const review = useReviewCandidate();
  const { logout } = useAuth();

  const submit = (event: FormEvent) => {
    event.preventDefault();
    discover.mutate(
      { sector, country },
      {
        onSuccess: (found) => {
          const existingOnly = found.length > 0 && found.every((candidate) => candidate.status === "existing");
          if (existingOnly) {
            toast(`AI search is rate-limited right now — showing ${found.length} match${found.length === 1 ? "" : "es"} already in your directory instead`, { icon: "⚠️" });
          } else {
            toast.success(found.length ? `Found ${found.length} candidate${found.length === 1 ? "" : "s"} to review` : "No new candidates found for that search");
          }
        },
        onError: () => toast.error("Discovery search failed. Please try again."),
      },
    );
  };

  const handleReview = (id: number, action: "approve" | "reject") => {
    review.mutate(
      { id, action },
      {
        onSuccess: () => toast.success(action === "approve" ? "Company approved and indexed" : "Candidate rejected"),
        onError: () => toast.error("Could not update this candidate. Please try again."),
      },
    );
  };

  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
        <div>
          <p className="text-sm font-medium text-cyan-300">Admin workspace</p>
          <h1 className="mt-2 text-3xl font-semibold text-white">Company discovery and review</h1>
          <p className="mt-2 max-w-2xl text-zinc-400">Review evidence before a company is added to the directory and indexed for Ask AI.</p>
        </div>

        <div className="flex shrink-0 gap-2">
          <Button variant="secondary" asChild>
            <Link href="/admin/companies">
              <Database className="h-4 w-4" />
              Data management
            </Link>
          </Button>
          <Button variant="secondary" onClick={logout}>
            <LogOut className="h-4 w-4" />
            Logout
          </Button>
        </div>
      </div>

      <Card className="hover:translate-y-0">
        <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-zinc-500">Discover companies</h2>
        <form onSubmit={submit} className="grid gap-4 md:grid-cols-[1fr_1fr_auto] md:items-end">
          <div>
            <label htmlFor="discover-sector" className="mb-1.5 block text-sm text-zinc-400">Sector</label>
            <Input id="discover-sector" value={sector} onChange={(e) => setSector(e.target.value)} placeholder="e.g. Dairy Processing" className="h-12" />
          </div>
          <div>
            <label htmlFor="discover-country" className="mb-1.5 block text-sm text-zinc-400">Country</label>
            <Input id="discover-country" value={country} onChange={(e) => setCountry(e.target.value)} placeholder="e.g. Germany" className="h-12" />
          </div>
          <Button type="submit" disabled={discover.isPending || !sector.trim() || !country.trim()} className="h-12">
            <Search className="h-4 w-4" />
            {discover.isPending ? "Discovering..." : "Discover"}
          </Button>
        </form>
        {discover.isError ? (
          <p role="alert" className="mt-4 text-sm text-red-300">Discovery failed. Verify the AI services are configured and try again.</p>
        ) : null}
      </Card>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold text-white">Candidates</h2>

        {candidates.isLoading ? (
          <div className="space-y-3" aria-busy="true" aria-label="Loading candidates">
            <LoadingSkeleton className="h-32 w-full" />
            <LoadingSkeleton className="h-32 w-full" />
          </div>
        ) : candidates.isError ? (
          <EmptyState title="Could not load candidates" description="Something went wrong. Try refreshing the page." />
        ) : candidates.data?.length ? (
          <div className="space-y-4">
            {candidates.data.map((candidate) => (
              <Card key={candidate.id} className="hover:translate-y-0">
                <div className="flex flex-col justify-between gap-5 md:flex-row">
                  <div className="min-w-0 space-y-3">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="text-lg font-semibold text-white">{candidate.name}</h3>
                      <span className="rounded-full bg-cyan-400/10 px-2.5 py-1 text-xs text-cyan-300">
                        {Math.round(candidate.confidence_score * 100)}% {candidate.status === "existing" ? "match" : "confidence"}
                      </span>
                      {candidate.status === "existing" ? (
                        <span className="rounded-full bg-amber-400/10 px-2.5 py-1 text-xs uppercase tracking-wide text-amber-300">Already in directory</span>
                      ) : (
                        <span className="rounded-full bg-white/5 px-2.5 py-1 text-xs uppercase tracking-wide text-zinc-400">{candidate.status}</span>
                      )}
                    </div>
                    <p className="text-sm text-zinc-400">{candidate.category} · {candidate.country}</p>
                    <p className="text-sm leading-relaxed text-zinc-300">{candidate.use_cases}</p>
                    <div className="space-y-2 pt-1">
                      {candidate.evidence.map((evidence) => (
                        <a key={evidence.url} href={evidence.url} target="_blank" rel="noreferrer" className="block rounded-lg bg-black/20 p-3.5 text-sm leading-relaxed text-zinc-300 transition hover:text-cyan-300">
                          <span className="font-medium">{evidence.source}</span>: {evidence.snippet} <ExternalLink className="ml-1 inline h-3.5 w-3.5" />
                        </a>
                      ))}
                    </div>
                  </div>
                  {candidate.status === "pending" ? (
                    <div className="flex shrink-0 gap-2">
                      <Button
                        onClick={() => handleReview(candidate.id, "approve")}
                        disabled={review.isPending}
                      >
                        <Check className="h-4 w-4" />
                        Approve
                      </Button>
                      <Button
                        variant="danger"
                        onClick={() => handleReview(candidate.id, "reject")}
                        disabled={review.isPending}
                      >
                        <X className="h-4 w-4" />
                        Reject
                      </Button>
                    </div>
                  ) : null}
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <EmptyState title="No candidates yet" description="Start a discovery search above to find real, evidence-backed AI vendors." />
        )}
      </section>
    </div>
  );
}
