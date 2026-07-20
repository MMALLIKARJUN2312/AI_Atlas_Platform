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
type FieldConfig = { name: keyof CompanyFormValues; label: string; required?: boolean; hint?: string };

const IDENTITY_FIELDS: FieldConfig[] = [
  { name: "vendor_name", label: "Vendor name", required: true },
  { name: "country", label: "Country", required: true },
  { name: "website", label: "Website", required: true, hint: "e.g. company.com" },
  { name: "company_type", label: "Company type", hint: "e.g. Incumbent, NewCo" },
];

const AI_PROFILE_FIELDS: FieldConfig[] = [
  { name: "ai_category", label: "AI category", required: true },
  { name: "segment_tags", label: "Segment tags", hint: "Comma-separated, e.g. 1,2,9", required: true },
  { name: "maturity", label: "Maturity" },
];

const BUSINESS_FIELDS: FieldConfig[] = [
  { name: "germany_presence", label: "Germany presence" },
  { name: "funding", label: "Funding" },
  { name: "estimated_revenue", label: "Estimated revenue" },
  { name: "top_germany_food_beverage_customers", label: "Top Germany F&B customers" },
];

const TEXTAREA_FIELDS: FieldConfig[] = [
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

  const errorCount = Object.keys(errors).length;

  function renderField(field: FieldConfig) {
    const errorId = `${field.name}-error`;
    const hasError = Boolean(errors[field.name]);

    return (
      <div key={field.name}>
        <label htmlFor={field.name} className="mb-1.5 block text-sm text-zinc-400">
          {field.label}
          {field.required ? <span className="ml-0.5 text-red-300">*</span> : null}
          {field.hint ? <span className="ml-2 text-xs text-zinc-600">{field.hint}</span> : null}
        </label>
        <Input
          id={field.name}
          aria-invalid={hasError}
          aria-describedby={hasError ? errorId : undefined}
          {...register(field.name)}
        />
        {hasError ? (
          <p id={errorId} role="alert" className="mt-1.5 text-xs text-red-300">
            {errors[field.name]?.message}
          </p>
        ) : null}
      </div>
    );
  }

  function renderTextarea(field: FieldConfig) {
    const errorId = `${field.name}-error`;
    const hasError = Boolean(errors[field.name]);

    return (
      <div key={field.name}>
        <label htmlFor={field.name} className="mb-1.5 block text-sm text-zinc-400">
          {field.label}
          {field.required ? <span className="ml-0.5 text-red-300">*</span> : null}
        </label>
        <textarea
          id={field.name}
          rows={3}
          aria-invalid={hasError}
          aria-describedby={hasError ? errorId : undefined}
          {...register(field.name)}
          className="w-full rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-3 text-white placeholder:text-slate-500 outline-none backdrop-blur-xl focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/20"
        />
        {hasError ? (
          <p id={errorId} role="alert" className="mt-1.5 text-xs text-red-300">
            {errors[field.name]?.message}
          </p>
        ) : null}
      </div>
    );
  }

  return (
    <form onSubmit={submit} noValidate className="space-y-8">
      <fieldset className="space-y-4">
        <legend className="text-sm font-semibold uppercase tracking-wide text-zinc-500">Company identity</legend>
        <div className="grid gap-4 sm:grid-cols-2">{IDENTITY_FIELDS.map(renderField)}</div>
      </fieldset>

      <fieldset className="space-y-4">
        <legend className="text-sm font-semibold uppercase tracking-wide text-zinc-500">AI profile</legend>
        <div className="grid gap-4 sm:grid-cols-2">{AI_PROFILE_FIELDS.map(renderField)}</div>
        <div className="space-y-4">{TEXTAREA_FIELDS.map(renderTextarea)}</div>
      </fieldset>

      <fieldset className="space-y-4">
        <legend className="text-sm font-semibold uppercase tracking-wide text-zinc-500">Business details</legend>
        <div className="grid gap-4 sm:grid-cols-2">{BUSINESS_FIELDS.map(renderField)}</div>
      </fieldset>

      <div className="flex flex-wrap items-center gap-3 border-t border-white/5 pt-6">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : company ? "Save changes" : "Add company"}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
        {errorCount > 0 ? (
          <p role="alert" className="text-sm text-red-300">
            {errorCount === 1 ? "1 field needs" : `${errorCount} fields need`} your attention.
          </p>
        ) : null}
      </div>
    </form>
  );
}
