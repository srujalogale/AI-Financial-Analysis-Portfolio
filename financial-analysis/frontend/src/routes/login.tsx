import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Eye, EyeOff, Sparkles, Mail, Lock, ArrowRight, CheckCircle2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

export const Route = createFileRoute("/login")({
  head: () => ({ meta: [{ title: "Sign in — AI financial Portfolio" }, { name: "description", content: "Sign in to AI financial Portfolio." }] }),
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const [show, setShow] = useState(false);
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.includes("@")) return setError("Please enter a valid email.");
    if (password.length < 6) return setError("Password must be at least 6 characters.");
    setError("");
    toast.success(mode === "login" ? "Signed in" : "Account created", { description: "Welcome to AI financial Portfolio." });
    navigate({ to: "/" });
  };

  return (
    <div className="flex min-h-screen w-full">
      {/* Left brand panel */}
      <div className="relative hidden flex-1 overflow-hidden border-r border-border bg-gradient-to-br from-background via-surface to-background lg:flex">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,oklch(0.78_0.16_220_/_0.25),transparent_55%),radial-gradient(circle_at_80%_80%,oklch(0.74_0.14_295_/_0.2),transparent_55%)]" />
        <div className="relative z-10 flex flex-col justify-between p-12">
          <Link to="/" className="flex items-center gap-2.5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-info shadow-[var(--shadow-glow)]">
              <Sparkles className="h-5 w-5 text-primary-foreground" />
            </div>
            <div>
              <p className="font-display text-lg font-bold">AI financial Portfolio</p>
              <p className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">AI Wealth</p>
            </div>
          </Link>

          <div className="space-y-6">
            <h1 className="font-display text-5xl font-bold leading-tight">
              Your AI <span className="gradient-text">portfolio advisor</span>, available 24/7.
            </h1>
            <p className="max-w-md text-base text-muted-foreground">
              Join 50,000+ investors who use AI financial Portfolio to build smarter, risk-aware portfolios.
            </p>
            <ul className="space-y-3">
              {["Personalized AI recommendations", "Real-time risk monitoring", "Monte Carlo simulations", "Sentiment-driven insights"].map((t) => (
                <li key={t} className="flex items-center gap-2.5 text-sm">
                  <CheckCircle2 className="h-4 w-4 text-success" />
                  <span className="text-muted-foreground">{t}</span>
                </li>
              ))}
            </ul>
          </div>

          <p className="text-xs text-muted-foreground">© 2026 AI financial Portfolio Inc. Securities offered through AI financial Portfolio Brokerage LLC.</p>
        </div>
      </div>

      {/* Right form panel */}
      <div className="flex w-full items-center justify-center bg-background px-6 py-10 lg:w-[480px] lg:px-10">
        <div className="w-full max-w-sm animate-fade-in">
          <div className="mb-8 flex lg:hidden">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-info">
              <Sparkles className="h-5 w-5 text-primary-foreground" />
            </div>
          </div>

          <div className="mb-6 inline-flex rounded-full border border-border bg-surface p-1">
            {(["login", "register"] as const).map((m) => (
              <button
                key={m}
                onClick={() => setMode(m)}
                className={`rounded-full px-4 py-1.5 text-xs font-semibold transition-all ${
                  mode === m ? "bg-primary text-primary-foreground shadow-[var(--shadow-glow)]" : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {m === "login" ? "Sign In" : "Create Account"}
              </button>
            ))}
          </div>

          <h2 className="font-display text-3xl font-bold tracking-tight">
            {mode === "login" ? "Welcome back" : "Get started"}
          </h2>
          <p className="mt-2 text-sm text-muted-foreground">
            {mode === "login" ? "Sign in to access your portfolio dashboard." : "Create a free account in under 60 seconds."}
          </p>

          <form onSubmit={submit} className="mt-8 space-y-4">
            {mode === "register" && (
              <div className="space-y-1.5">
                <Label htmlFor="name" className="text-xs uppercase tracking-wider text-muted-foreground">Full Name</Label>
                <Input id="name" placeholder="Alex Rivera" className="h-11 border-border/60 bg-surface" />
              </div>
            )}

            <div className="space-y-1.5">
              <Label htmlFor="email" className="text-xs uppercase tracking-wider text-muted-foreground">Email</Label>
              <div className="relative">
                <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@email.com"
                  className="h-11 border-border/60 bg-surface pl-9"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-xs uppercase tracking-wider text-muted-foreground">Password</Label>
                {mode === "login" && (
                  <button
                    type="button"
                    onClick={() => toast.message("Reset link sent", { description: "Check your inbox for password reset instructions." })}
                    className="text-[11px] text-primary hover:underline"
                  >
                    Forgot?
                  </button>
                )}
              </div>
              <div className="relative">
                <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  id="password" type={show ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="h-11 border-border/60 bg-surface pl-9 pr-10"
                />
                <button type="button" onClick={() => setShow(!show)} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
                  {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {error && (
              <div className="rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive">{error}</div>
            )}

            <Button type="submit" className="h-11 w-full bg-gradient-to-r from-primary to-info text-primary-foreground shadow-[var(--shadow-glow)] hover:opacity-90">
              {mode === "login" ? "Sign In" : "Create Account"}
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>

            <div className="relative my-2 flex items-center">
              <div className="flex-1 border-t border-border" />
              <span className="px-3 text-[10px] uppercase tracking-wider text-muted-foreground">or</span>
              <div className="flex-1 border-t border-border" />
            </div>

            <Button
              type="button"
              variant="outline"
              className="h-11 w-full border-border bg-surface hover:bg-surface-elevated"
              onClick={() => {
                toast.success("Signed in with Google");
                navigate({ to: "/" });
              }}
            >
              Continue with Google
            </Button>
          </form>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            By continuing you agree to our{" "}
            <button type="button" onClick={() => toast.message("Terms of Service")} className="text-primary hover:underline">Terms</button>{" "}
            and{" "}
            <button type="button" onClick={() => toast.message("Privacy Policy")} className="text-primary hover:underline">Privacy</button>.
          </p>
        </div>
      </div>
    </div>
  );
}
