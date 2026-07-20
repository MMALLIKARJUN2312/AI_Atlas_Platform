"use client";

import { ReactNode, useEffect } from "react";
import { useRouter } from "next/navigation";

import { LoadingSpinner } from "@/components/ui";
import { getStoredToken } from "@/lib/auth-storage";
import { useAuth } from "@/providers/auth-provider";

export function AdminGuard({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // On a hard navigation, this effect can run before useSyncExternalStore's
    // hydration correction lands, so isAuthenticated may still reflect the
    // (token-less) server snapshot. Re-check localStorage directly here,
    // after mount, to avoid redirecting a genuinely logged-in admin away.
    if (!isAuthenticated && !getStoredToken()) {
      router.replace("/admin/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return <>{children}</>;
}
