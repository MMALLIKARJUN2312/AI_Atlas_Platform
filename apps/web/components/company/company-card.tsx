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
        rounded-xl border border-white/10 bg-zinc-900/70 p-5
        transition-colors
        hover:border-sky-400/40
      "
    >
      <div className="flex items-start justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-sky-400/10">
          <Building2
            size={22}
            className="text-sky-300"
          />
        </div>

        <Badge>{company.maturity}</Badge>
      </div>

      <div className="mt-5">
        <h2 className="line-clamp-2 text-lg font-semibold text-white">
          {company.vendor_name}
        </h2>

        <p className="mt-2 line-clamp-2 text-sm text-zinc-400">
          {company.ai_category}
        </p>
      </div>

      <div className="mt-5 flex items-center gap-2 text-sm text-zinc-400">
        <Globe size={16} />
        {company.country}
      </div>

      <p className="mt-3 text-sm text-zinc-500">{company.company_type}</p>
      {tags && (
        <div className="mt-4 flex flex-wrap gap-2">
          {tags.map((tag) => (
            <Tag
              key={tag}
              label={tag}
            />
          ))}
        </div>
      )}

      <div className="mt-auto pt-5">
        <div className="flex items-center justify-between border-t border-white/10 pt-4">
          <a
            href={company.website}
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1 text-sm text-zinc-400 hover:text-white"
          >
            Website
            <ExternalLink size={14} />
          </a>

          <Link
            href={`/companies/${company.id}`}
            className="flex items-center gap-2 rounded-md bg-white px-3 py-2 text-sm font-medium text-zinc-950 hover:bg-zinc-200"
          >
            View
            <ArrowRight size={16} />
          </Link>
        </div>
      </div>
    </motion.article>
  );
}
