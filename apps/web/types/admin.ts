import type { Company } from "./company";

export interface DiscoveryEvidence { source: string; snippet: string; url: string; }
export interface CompanyCandidate { id: number; name: string; country: string; category: string; segment_tags: string; use_cases: string; website: string; evidence: DiscoveryEvidence[]; confidence_score: number; status: "pending" | "approved" | "rejected"; }
export type CompanyWrite = Omit<Company, "id" | "created_at" | "updated_at">;
