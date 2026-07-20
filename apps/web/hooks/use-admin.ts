import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { adminService } from "@/services";
import type { CompanyWrite } from "@/types/admin";

export function useCandidates() { return useQuery({ queryKey: ["admin", "candidates"], queryFn: () => adminService.candidates() }); }
export function useDiscoverCompanies() { const queryClient = useQueryClient(); return useMutation({ mutationFn: ({ sector, country }: { sector: string; country: string }) => adminService.discover(sector, country), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin", "candidates"] }) }); }
export function useReviewCandidate() { const queryClient = useQueryClient(); return useMutation({ mutationFn: async ({ id, action }: { id: number; action: "approve" | "reject" }) => { await (action === "approve" ? adminService.approve(id) : adminService.reject(id)); }, onSuccess: () => queryClient.invalidateQueries({ queryKey: ["admin"] }) }); }
export function useSaveCompany() { const queryClient = useQueryClient(); return useMutation({ mutationFn: ({ id, company }: { id?: number; company: CompanyWrite }) => id ? adminService.updateCompany(id, company) : adminService.createCompany(company), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["companies"] }) }); }
