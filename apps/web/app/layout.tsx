import type { Metadata } from "next";
import { ReactNode } from "react";

import "@/styles/globals.css";

import { QueryProvider } from "@/providers/query-provider";
import { ToastProvider } from "@/providers/toast-provider";
import { AuthProvider } from "@/providers/auth-provider";

import { AppShell } from "@/components/layout";

export const metadata: Metadata = {
  title: "AI Atlas",
  description: "AI Atlas Platform",
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>
          <AuthProvider>
            <ToastProvider />
            <AppShell>{children}</AppShell>
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}