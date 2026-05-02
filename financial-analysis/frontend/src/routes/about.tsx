import { createFileRoute } from "@tanstack/react-router";
import { Sparkles, Brain, Shield, Activity, TrendingUp } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";

export const Route = createFileRoute("/about")({
  head: () => ({ meta: [{ title: "About — AI financial Portfolio" }, { name: "description", content: "About AI financial Portfolio platform." }] }),
  component: AboutPage,
});

const features = [
  { icon: Brain, title: "AI Recommendations", desc: "Transformer-based models analyze 10k+ signals daily to build optimal portfolios." },
  { icon: Shield, title: "Risk-Aware", desc: "VaR, CVaR, and stress tests run continuously to keep you within tolerance." },
  { icon: Activity, title: "Monte Carlo", desc: "Simulate 10,000 paths in under 3s for confident planning." },
  { icon: TrendingUp, title: "Real-Time Tracking", desc: "Sub-second market data with smart alerts for what matters." },
];

function AboutPage() {
  return (
    <AppShell>
      <PageHeader eyebrow="About" title="AI financial Portfolio" description="Institutional-grade portfolio intelligence, built for everyone." />

      <div className="glass-card relative mb-6 overflow-hidden rounded-3xl p-10">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_30%_0%,oklch(0.78_0.16_220_/_0.18),transparent_60%)]" />
        <div className="relative max-w-2xl">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-semibold text-primary">
            <Sparkles className="h-3.5 w-3.5" />v3.2 — April 2026
          </div>
          <h2 className="font-display text-4xl font-bold leading-tight">
            Smarter portfolios, <span className="gradient-text">powered by AI</span>.
          </h2>
          <p className="mt-3 text-base text-muted-foreground">
            AI financial Portfolio combines reinforcement learning with classical portfolio theory to deliver personalized,
            risk-adjusted recommendations — explained in plain English.
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {features.map((f) => (
          <SectionCard key={f.title}>
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary/20 to-info/10 text-primary">
              <f.icon className="h-5 w-5" />
            </div>
            <p className="mt-3 font-display text-base font-bold">{f.title}</p>
            <p className="mt-1 text-sm text-muted-foreground">{f.desc}</p>
          </SectionCard>
        ))}
      </div>

      <SectionCard title="Built with" description="Production-grade stack" className="mt-6">
        <div className="flex flex-wrap gap-2">
          {["React 19", "TanStack Router", "Tailwind v4", "Recharts", "shadcn/ui", "Lucide", "TypeScript"].map((t) => (
            <span key={t} className="rounded-full border border-border bg-surface px-3 py-1 text-xs font-medium text-muted-foreground">{t}</span>
          ))}
        </div>
      </SectionCard>
    </AppShell>
  );
}
