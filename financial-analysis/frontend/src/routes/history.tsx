import { createFileRoute } from "@tanstack/react-router";
import { Clock, ArrowUpRight } from "lucide-react";
import { LineChart, Line, ResponsiveContainer, XAxis, YAxis, CartesianGrid, Tooltip as RTooltip } from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Badge } from "@/components/ui/badge";
import { history, portfolioGrowth } from "@/lib/mock-data";

export const Route = createFileRoute("/history")({
  head: () => ({ meta: [{ title: "History — AI financial Portfolio" }, { name: "description", content: "Past portfolios and performance timeline." }] }),
  component: HistoryPage,
});

function HistoryPage() {
  return (
    <AppShell>
      <PageHeader eyebrow="History" title="Performance Timeline" description="Track every portfolio version and its real-world results." />

      <SectionCard title="Lifetime Growth" description="From inception to today" className="mb-6">
        <div className="h-[260px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={portfolioGrowth} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--chart-grid)" />
              <XAxis dataKey="day" tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "var(--chart-axis)", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
              <RTooltip contentStyle={{ background: "var(--chart-tooltip-bg)", border: "1px solid var(--chart-tooltip-border)", borderRadius: 12, fontSize: 12 }} />
              <Line dataKey="portfolio" stroke="var(--chart-1)" strokeWidth={2.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </SectionCard>

      <div className="relative">
        <div className="absolute bottom-0 left-[19px] top-2 w-px bg-border" />
        <div className="space-y-4">
          {history.map((h) => (
            <div key={h.id} className="relative flex items-start gap-5">
              <div className="relative z-10 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-border bg-surface">
                <Clock className="h-4 w-4 text-primary" />
              </div>
              <div className="glass-card flex-1 rounded-2xl p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-display text-base font-bold">{h.name}</p>
                      <Badge variant="outline" className={h.status === "Active" ? "border-success/30 bg-success/15 text-success" : "border-border text-muted-foreground"}>
                        {h.status}
                      </Badge>
                    </div>
                    <p className="mt-0.5 text-xs text-muted-foreground">{h.date}</p>
                  </div>
                  <div className="flex items-center gap-6 text-right">
                    <div>
                      <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Value</p>
                      <p className="font-display text-lg font-bold tabular-nums">${h.value.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Return</p>
                      <p className={`inline-flex items-center gap-1 font-mono text-base font-bold ${h.return >= 0 ? "text-success" : "text-destructive"}`}>
                        {h.return >= 0 && <ArrowUpRight className="h-4 w-4" />}+{h.return}%
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
