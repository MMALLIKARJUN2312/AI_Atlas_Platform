"use client";

import Link from "next/link";
import {
  ArrowRight,
  Building2,
  ExternalLink,
  Globe,
} from "lucide-react";
import { motion } from "framer-motion";

import { Badge } from "@/components/ui";
import { externalUrl } from "@/lib/utils";
import { Company } from "@/types/company";

interface CompanyCardProps {
  company: Company;
}

function Tag({
  label,
}: {
  label: string;
}) {
  return (
    <span className="rounded-md bg-zinc-800 px-2.5 py-1 text-xs text-zinc-300">
      {label}
    </span>
  );
}

export function CompanyCard({
  company,
}: CompanyCardProps) {
  const tags =
    company.segment_tags
      ?.split(",")
      .map((tag) => tag.trim())
      .slice(0, 3);

  return (
    <motion.article
      whileHover={{
        y: -2,
      }}
      transition={{
        duration: 0.18,
      }}
      className="
        flex
        h-full
        flex-col
        rounded-xl border border-white/10 bg-zinc-900/70 p-6
        transition-colors
        hover:border-sky-400/40
      "
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-sky-400/10">
          <Building2
            size={22}
            className="text-sky-300"
          />
        </div>

        <Badge className="shrink-0">{company.maturity}</Badge>
      </div>

      <div className="mt-5 space-y-4">
        <div>
          <h2 className="line-clamp-2 text-lg font-semibold leading-snug text-white">
            {company.vendor_name}
          </h2>

          <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-zinc-400">
            {company.ai_category}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-sm text-zinc-400">
          <span className="flex items-center gap-1.5">
            <Globe size={16} />
            {company.country}
          </span>
          <span className="text-zinc-500">{company.company_type}</span>
        </div>

        {tags && tags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {tags.map((tag) => (
              <Tag
                key={tag}
                label={tag}
              />
            ))}
          </div>
        )}
      </div>

      <div className="mt-auto pt-6">
        <div className="flex items-center justify-between border-t border-white/10 pt-5">
          {company.website ? (
            <a
              href={externalUrl(company.website)}
              target="_blank"
              rel="noreferrer"
              onClick={(event) => event.stopPropagation()}
              className="flex items-center gap-1 text-sm text-zinc-400 hover:text-white"
            >
              Website
              <ExternalLink size={14} />
            </a>
          ) : (
            <span />
          )}

          <Link
            href={`/companies/${company.id}`}
            className="flex items-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-medium text-zinc-950 transition hover:bg-zinc-200"
          >
            View
            <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </motion.article>
  );
}
