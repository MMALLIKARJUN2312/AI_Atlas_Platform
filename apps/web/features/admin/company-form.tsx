"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button, Input } from "@/components/ui";
import type { Company } from "@/types/company";
import type { CompanyWrite } from "@/types/admin";

const companyFormSchema = z.object({
  vendor_name: z.string().min(1, "Vendor name is required"),
  country: z.string().min(1, "Country is required"),
  ai_category: z.string().min(1, "AI category is required"),
  segment_tags: z.string().min(1, "Segment tags are required"),
  food_beverage_ai_use_case: z.string().min(1, "AI use case is required"),
  website: z.string().min(1, "Website is required"),
  germany_presence: z.string().optional(),
  company_type: z.string().optional(),
  top_germany_food_beverage_customers: z.string().optional(),
  funding: z.string().optional(),
  estimated_revenue: z.string().optional(),
  maturity: z.string().optional(),
  top_deployment_evidence: z.string().optional(),
});

type CompanyFormValues = z.infer<typeof companyFormSchema>;

const FIELDS: { name: keyof CompanyFormValues; label: string; required?: boolean }[] = [
  { name: "vendor_name", label: "Vendor name", required: true },
  { name: "country", label: "Country", required: true },
  { name: "website", label: "Website", required: true },
  { name: "ai_category", label: "AI category", required: true },
  { name: "segment_tags", label: "Segment tags (comma-separated)", required: true },
  { name: "company_type", label: "Company type" },
  { name: "germany_presence", label: "Germany presence" },
  { name: "maturity", label: "Maturity" },
  { name: "funding", label: "Funding" },
  { name: "estimated_revenue", label: "Estimated revenue" },
  { name: "top_germany_food_beverage_customers", label: "Top Germany F&B customers" },
];

const TEXTAREA_FIELDS: { name: keyof CompanyFormValues; label: string; required?: boolean }[] = [
  { name: "food_beverage_ai_use_case", label: "F&B AI use case", required: true },
  { name: "top_deployment_evidence", label: "Deployment evidence" },
];

interface CompanyFormProps {
  company?: Company;
  onSubmit: (values: CompanyWrite) => void;
  onCancel: () => void;
  isSubmitting: boolean;
}

export function CompanyForm({ company, onSubmit, onCancel, isSubmitting }: CompanyFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CompanyFormValues>({
    resolver: zodResolver(companyFormSchema),
    defaultValues: {
      vendor_name: company?.vendor_name ?? "",
      country: company?.country ?? "",
      ai_category: company?.ai_category ?? "",
      segment_tags: company?.segment_tags ?? "",
      germany_presence: company?.germany_presence ?? "",
      company_type: company?.company_type ?? "NewCo",
      food_beverage_ai_use_case: company?.food_beverage_ai_use_case ?? "",
      top_germany_food_beverage_customers: company?.top_germany_food_beverage_customers ?? "",
      funding: company?.funding ?? "Not disclosed",
      estimated_revenue: company?.estimated_revenue ?? "Not disclosed",
      maturity: company?.maturity ?? "Unknown",
      top_deployment_evidence: company?.top_deployment_evidence ?? "",
      website: company?.website ?? "",
    },
  });

  const submit = handleSubmit((values) => {
    onSubmit({
      ...values,
      germany_presence: values.germany_presence ?? "",
      company_type: values.company_type || "NewCo",
      top_germany_food_beverage_customers: values.top_germany_food_beverage_customers ?? "",
      funding: values.funding || "Not disclosed",
      estimated_revenue: values.estimated_revenue || "Not disclosed",
      maturity: values.maturity || "Unknown",
      top_deployment_evidence: values.top_deployment_evidence ?? "",
    });
  });

  return (
    <form onSubmit={submit} className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2">
        {FIELDS.map((field) => (
          <div key={field.name}>
            <label className="mb-1.5 block text-sm text-zinc-400">
              {field.label}
              {field.required ? <span className="text-red-300"> *</span> : null}
            </label>
            <Input {...register(field.name)} />
            {errors[field.name] ? <p className="mt-1 text-xs text-red-300">{errors[field.name]?.message}</p> : null}
          </div>
        ))}
      </div>

      {TEXTAREA_FIELDS.map((field) => (
        <div key={field.name}>
          <label className="mb-1.5 block text-sm text-zinc-400">
            {field.label}
            {field.required ? <span className="text-red-300"> *</span> : null}
          </label>
          <textarea
            {...register(field.name)}
            rows={3}
            className="w-full rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-3 text-white placeholder:text-slate-500 outline-none backdrop-blur-xl focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20"
          />
          {errors[field.name] ? <p className="mt-1 text-xs text-red-300">{errors[field.name]?.message}</p> : null}
        </div>
      ))}

      <div className="flex gap-3">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : company ? "Save changes" : "Add company"}
        </Button>
        <button
          type="button"
          onClick={onCancel}
          className="rounded-xl border border-white/10 px-4 py-2.5 text-sm text-zinc-300 hover:border-white/30"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
