import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Activity, Play, TrendingUp, TrendingDown } from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RTooltip, ResponsiveContainer,
  BarChart, Bar, Area, AreaChart,
} from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { monteCarlo, distribution } from "@/lib/mock-data";

export const Route = createFileRoute("/simulation")({
  head: () => ({ meta: [{ title: "Simulation — AI financial Portfolio" }, { name: "description", content: "Monte Carlo portfolio simulations and probability distributions." }] }),
  component: SimulationPage,
});

const tooltipStyle = {
  contentStyle: {
    background: "var(--chart-tooltip-bg)",
    border: "1px solid var(--chart-tooltip-border)",
    borderRadius: 12,
    fontSize: 12,
    boxShadow: "0 10px 30px -10px oklch(0.30 0.05 248 / 0.18)",
  },
  labelStyle: { color: "var(--foreground)", fontWeight: 600 },
};

function SimulationPage() {
  const [horizon, setHorizon] = useState([60]);
  const [runs, setRuns] = useState([1000]);
  const [running, setRunning] = useState(false);

  const runSim = () => {
    setRunning(true);
    const t = toast.loading("Running Monte Carlo simulation…", {
      description: `${runs[0].toLocaleString()} paths over ${horizon[0]} days`,
    });
    setTimeout(() => {
      toast.success("Simulation complete", { id: t, description: "82.4% probability of exceeding goal." });
      setRunning(false);
    }, 1400);
  };

  return (
    <AppShell>
      <PageHeader
        eyebrow="Simulation"
        title="Monte Carlo Forecast"
        description="Project thousands of possible portfolio paths to understand range of outcomes."
        actions={
          <Button
            disabled={running}
            onClick={runSim}
            className="bg-gradient-to-r from-primary to-info text-primary-foreground"
          >
            <Play className="mr-2 h-4 w-4" />{running ? "Running…" : "Run Simulation"}
          </Button>
        }
      />

      <div className="grid gap-4 md:grid-cols-4">
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">Best Case</p>
          <p className="mt-1 font-display text-2xl font-bold text-success">$268,400</p>
          <p className="mt-1 text-xs text-muted-foreground">95th percentile</p>
        </div>
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">Median</p>
          <p className="mt-1 font-display text-2xl font-bold">$184,200</p>
          <p className="mt-1 text-xs text-muted-foreground">50th percentile</p>
        </div>
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">Worst Case</p>
          <p className="mt-1 font-display text-2xl font-bold text-destructive">$92,800</p>
          <p className="mt-1 text-xs text-muted-foreground">5th percentile</p>
        </div>
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">Success Rate</p>
          <p className="mt-1 font-display text-2xl font-bold text-primary">82.4%</p>
          <p className="mt-1 text-xs text-muted-foreground">P(value &gt; goal)</p>
        </div>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <SectionCard title="Simulation Controls" description="Tune parameters">
          <div className="space-y-6">
            <div>
              <div className="mb-2 flex justify-between text-xs">
                <span className="text-muted-foreground">Time Horizon (days)</span>
                <span className="font-mono font-semibold">{horizon[0]}</span>
              </div>
              <Slider value={horizon} onValueChange={setHorizon} min={30} max={365} step={5} />
            </div>
            <div>
              <div className="mb-2 flex justify-between text-xs">
                <span className="text-muted-foreground">Simulation Runs</span>
                <span className="font-mono font-semibold">{runs[0].toLocaleString()}</span>
              </div>
              <Slider value={runs} onValueChange={setRuns} min={100} max={10000} step={100} />
            </div>
            <div className="rounded-xl border border-border/60 bg-surface/60 p-4">
              <div className="flex items-center gap-2 text-xs text-muted-foreground"><Activity className="h-3.5 w-3.5" /> Model</div>
              <p className="mt-1 text-sm font-semibold">Geometric Brownian Motion</p>
              <p className="mt-1 text-xs text-muted-foreground">μ = 8.4%, σ = 14.2% (annualized)</p>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <Badge className="border-success/30 bg-success/15 text-success justify-center py-1.5"><TrendingUp className="mr-1 h-3 w-3" />Bullish</Badge>
              <Badge className="border-destructive/30 bg-destructive/15 text-destructive justify-center py-1.5"><TrendingDown className="mr-1 h-3 w-3" />Bearish</Badge>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Projected Paths" description="Best / Worst / Median across 1,000 runs" className="xl:col-span-2">
          <div className="h-[320px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monteCarlo} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
                <defs>
                  <linearGradient id="gMed" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid)" />
                <XAxis dataKey="day" tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                <RTooltip {...tooltipStyle} formatter={(v: number) => `$${v.toLocaleString()}`} />
                {Array.from({ length: 12 }).map((_, i) => (
                  <Line key={i} dataKey={`p${i}`} stroke={`var(--chart-${(i % 5) + 1})`} strokeWidth={1} dot={false} strokeOpacity={0.25} />
                ))}
                <Area type="monotone" dataKey="median" stroke="var(--chart-1)" strokeWidth={2.5} fill="url(#gMed)" />
                <Line dataKey="best" stroke="var(--chart-2)" strokeWidth={2} strokeDasharray="5 5" dot={false} />
                <Line dataKey="worst" stroke="var(--chart-5)" strokeWidth={2} strokeDasharray="5 5" dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Probability Distribution" description="Histogram of terminal portfolio values" className="mt-6">
        <div className="h-[280px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={distribution} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
              <defs>
                <linearGradient id="gBar" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--chart-1)" stopOpacity={1} />
                  <stop offset="100%" stopColor="var(--chart-3)" stopOpacity={0.6} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid)" />
              <XAxis dataKey="bucket" tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} />
              <RTooltip {...tooltipStyle} />
              <Bar dataKey="probability" fill="url(#gBar)" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </SectionCard>
    </AppShell>
  );
}
