import type { Metadata } from "next";
import { ReactNode } from "react";

import { QueryProvider } from "@/providers/query-provider";
import { ToastProvider } from "@/providers/toast-provider";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Atlas",
  description: "Production-grade AI-powered intelligence platform for businesses and organizations.",
};

type Props = {
  children: ReactNode;
};

export default function RootLayout({ children }: Props) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>
          <ToastProvider />
          {children}
        </QueryProvider>
      </body>
    </html>
  );
}