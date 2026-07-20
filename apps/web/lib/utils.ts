import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Dataset website values are often bare domains (e.g. "gea.com") with no
 * protocol, which resolves as a broken relative link when used as an <a href>.
 * Normalize to an absolute https URL before rendering as an external link.
 */
export function externalUrl(value: string | null | undefined): string {
  const trimmed = (value ?? "").trim();
  if (!trimmed) return "";
  return /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
}