import { AppShell } from "@/components/layout";

export default function HomePage() {
  return (
    <AppShell>

      <div className="space-y-4">

        <h1 className="text-5xl font-bold text-white">
          Welcome to AI Atlas
        </h1>

        <p className="max-w-3xl text-zinc-400">
          Discover AI companies, explore industry problems,
          and interact with an AI-powered knowledge platform
          built for the German Food & Beverage ecosystem.
        </p>

      </div>

    </AppShell>
  );
}