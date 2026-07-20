"use client";

import { type FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldCheck } from "lucide-react";

import { Button, GlassPanel, Input } from "@/components/ui";
import { useAuth } from "@/providers/auth-provider";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login(email, password);
      router.replace("/admin");
    } catch {
      setError("Incorrect email or password.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="mx-auto flex min-h-full max-w-md flex-col items-center justify-center">
      <GlassPanel className="w-full">
        <div className="flex flex-col items-center gap-2 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-300">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-semibold text-white">Admin sign in</h1>
          <p className="text-sm text-zinc-400">Sign in to review discovery candidates and manage companies.</p>
        </div>

        <form onSubmit={submit} noValidate className="mt-8 space-y-4">
          <div>
            <label htmlFor="login-email" className="mb-1.5 block text-sm text-zinc-400">Email</label>
            <Input
              id="login-email"
              type="email"
              required
              placeholder="you@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="username"
              aria-invalid={Boolean(error)}
            />
          </div>
          <div>
            <label htmlFor="login-password" className="mb-1.5 block text-sm text-zinc-400">Password</label>
            <Input
              id="login-password"
              type="password"
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              aria-invalid={Boolean(error)}
              aria-describedby={error ? "login-error" : undefined}
            />
          </div>

          {error ? <p id="login-error" role="alert" className="text-sm text-red-300">{error}</p> : null}

          <Button type="submit" disabled={isSubmitting} className="w-full">
            {isSubmitting ? "Signing in..." : "Sign in"}
          </Button>
        </form>
      </GlassPanel>
    </div>
  );
}
