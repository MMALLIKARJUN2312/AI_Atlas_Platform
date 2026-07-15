import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Atlas",
  description: "Production-grade AI-powered intelligence platform for businesses and organizations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
    >
      <body>{children}</body>
    </html>
  );
}
