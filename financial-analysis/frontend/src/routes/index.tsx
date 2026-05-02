import { createFileRoute, Link } from "@tanstack/react-router";
import { toast } from "sonner";
import {
  Wallet, TrendingUp, AlertTriangle, Target, Sparkles, ArrowUpRight, RefreshCw, Bell,
} from "lucide-react";
import {
  PieChart, Pie, Cell, Tooltip as RTooltip, ResponsiveContainer,
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  ScatterChart, Scatter, ZAxis,
} from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { StatCard } from "@/components/ui-kit/StatCard";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { allocation, portfolioGrowth, riskReturn, alerts } from "@/lib/mock-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Dashboard — AI financial Portfolio" },
      { name: "description", content: "AI-powered portfolio recommendations, risk analytics, and real-time tracking." },
    ],
  }),
  component: Dashboard,
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
  itemStyle: { color: "var(--foreground)" },
};

function Dashboard() {
  return (
    <AppShell>
      <PageHeader
        eyebrow="Overview"
        title="Welcome back, Alex"
        description="Your AI advisor has 3 new recommendations and detected 2 risk events overnight."
        actions={
          <>
            <Button
              variant="outline"
              className="border-border bg-surface hover:bg-surface-elevated"
              onClick={() => toast.success("Portfolio refreshed", { description: "Latest market data synced." })}
            >
              <RefreshCw className="mr-2 h-4 w-4" /> Refresh
            </Button>
            <Button
              className="bg-gradient-to-r from-primary to-info text-primary-foreground shadow-[var(--shadow-glow)] hover:opacity-90"
              onClick={() => toast.message("Generating AI plan…", { description: "Your personalized strategy will be ready in a moment." })}
            >
              <Sparkles className="mr-2 h-4 w-4" /> Get AI Plan
            </Button>
          </>
        }
      />

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Total Investment" value="$125,000" change={0} hint="Capital deployed" icon={<Wallet className="h-5 w-5" />} />
        <StatCard label="Current Value" value="$142,830" change={14.26} hint="vs initial" icon={<TrendingUp className="h-5 w-5" />} tone="success" />
        <StatCard label="Profit / Loss" value="+$17,830" change={4.82} hint="this month" icon={<ArrowUpRight className="h-5 w-5" />} tone="success" />
        <StatCard label="Risk Level" value="Moderate" change={-1.4} hint="Volatility 14.2%" icon={<AlertTriangle className="h-5 w-5" />} tone="warning" />
      </div>

      {/* Charts */}
      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <SectionCard title="Portfolio Allocation" description="AI-optimized weighting" className="xl:col-span-1">
          <div className="h-[260px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={allocation} dataKey="value" innerRadius={62} outerRadius={92} paddingAngle={3} stroke="none">
                  {allocation.map((e, i) => <Cell key={i} fill={e.color} />)}
                </Pie>
                <RTooltip {...tooltipStyle} formatter={(v: number) => `${v}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-3 grid grid-cols-2 gap-2">
            {allocation.map((a) => (
              <div key={a.name} className="flex items-center justify-between gap-2 rounded-lg border border-border/50 bg-surface/60 px-2.5 py-1.5">
                <div className="flex items-center gap-2 truncate">
                  <span className="h-2 w-2 rounded-full" style={{ background: a.color }} />
                  <span className="truncate text-xs text-muted-foreground">{a.name}</span>
                </div>
                <span className="font-mono text-xs font-semibold">{a.value}%</span>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard
          title="Portfolio Growth"
          description="Last 30 days vs benchmark"
          className="xl:col-span-2"
          action={<Badge className="border-success/30 bg-success/15 text-success">+14.26%</Badge>}
        >
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={portfolioGrowth} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
                <defs>
                  <linearGradient id="gPort" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--chart-1)" stopOpacity={0.5} />
                    <stop offset="95%" stopColor="var(--chart-1)" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gBench" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--chart-3)" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="var(--chart-3)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid)" />
                <XAxis dataKey="day" tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                <RTooltip {...tooltipStyle} formatter={(v: number) => `$${v.toLocaleString()}`} />
                <Area type="monotone" dataKey="benchmark" stroke="var(--chart-3)" strokeWidth={2} fill="url(#gBench)" strokeDasharray="4 4" />
                <Area type="monotone" dataKey="portfolio" stroke="var(--chart-1)" strokeWidth={2.5} fill="url(#gPort)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        <SectionCard title="Risk vs Return" description="Bubble size = position weight" className="lg:col-span-2">
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid)" />
                <XAxis type="number" dataKey="risk" name="Risk" unit="%" tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis type="number" dataKey="return" name="Return" unit="%" tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} />
                <ZAxis type="number" dataKey="size" range={[80, 400]} />
                <RTooltip {...tooltipStyle} cursor={{ strokeDasharray: "3 3", stroke: "var(--primary)" }} />
                <Scatter data={riskReturn} fill="var(--chart-1)">
                  {riskReturn.map((_, i) => <Cell key={i} fill={`var(--chart-${(i % 5) + 1})`} fillOpacity={0.85} />)}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>

        {/* AI Recommendation */}
        <SectionCard
          title="AI Recommendation"
          description="Generated 2 minutes ago"
          action={<Badge className="border-primary/30 bg-primary/15 text-primary">v3.2</Badge>}
        >
          <div className="space-y-4">
            <div className="rounded-xl border border-primary/20 bg-gradient-to-br from-primary/10 to-info/5 p-4">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/20"><Sparkles className="h-4 w-4 text-primary" /></div>
                <div>
                  <p className="text-xs uppercase tracking-wider text-muted-foreground">Suggested Strategy</p>
                  <p className="font-display text-lg font-bold">Aggressive Growth+</p>
                </div>
              </div>
            </div>

            {[
              { label: "Equities", val: 52, color: "var(--chart-1)" },
              { label: "Crypto", val: 18, color: "var(--chart-4)" },
              { label: "Bonds", val: 20, color: "var(--chart-3)" },
              { label: "Cash", val: 10, color: "var(--chart-2)" },
            ].map((r) => (
              <div key={r.label}>
                <div className="mb-1 flex justify-between text-xs">
                  <span className="text-muted-foreground">{r.label}</span>
                  <span className="font-mono font-semibold">{r.val}%</span>
                </div>
                <Progress value={r.val} className="h-1.5 bg-surface [&>div]:bg-[var(--primary)]" style={{ ["--primary" as any]: r.color }} />
              </div>
            ))}

            <div className="grid grid-cols-2 gap-2 pt-2">
              <div className="rounded-lg border border-border bg-surface p-2.5">
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Exp. Return</p>
                <p className="font-display text-lg font-bold text-success">+18.4%</p>
              </div>
              <div className="rounded-lg border border-border bg-surface p-2.5">
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Risk Score</p>
                <p className="font-display text-lg font-bold text-warning">7.2/10</p>
              </div>
            </div>

            <p className="rounded-lg border border-border/60 bg-background/40 p-3 text-xs leading-relaxed text-muted-foreground">
              <strong className="text-foreground">Why this portfolio?</strong> Tilted toward AI/semis given strong earnings momentum. BTC sleeve hedges USD weakness. Bond duration shortened on hawkish Fed.
            </p>

            <Button
              className="w-full bg-gradient-to-r from-primary to-info text-primary-foreground hover:opacity-90"
              onClick={() => toast.success("Recommendation applied", { description: "Aggressive Growth+ is now your active strategy." })}
            >
              Apply Recommendation <Target className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </SectionCard>
      </div>

      {/* Alerts */}
      <SectionCard
        title="Live Alerts"
        description="Market events and rebalancing signals"
        className="mt-6"
        action={<Button asChild variant="ghost" size="sm" className="text-primary hover:text-primary"><Link to="/alerts"><Bell className="mr-1.5 h-3.5 w-3.5" />View all</Link></Button>}
      >
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {alerts.slice(0, 3).map((a) => (
            <div key={a.id} className="group rounded-xl border border-border/60 bg-surface/60 p-4 transition-all hover:border-primary/30">
              <div className="flex items-start gap-3">
                <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${
                  a.severity === "high" ? "bg-destructive/15 text-destructive" :
                  a.severity === "medium" ? "bg-warning/15 text-warning" : "bg-info/15 text-info"
                }`}>
                  <AlertTriangle className="h-4 w-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold">{a.title}</p>
                  <p className="mt-0.5 text-xs text-muted-foreground">{a.desc}</p>
                  <p className="mt-2 font-mono text-[10px] uppercase tracking-wider text-muted-foreground/70">{a.time}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>
    </AppShell>
  );
}
