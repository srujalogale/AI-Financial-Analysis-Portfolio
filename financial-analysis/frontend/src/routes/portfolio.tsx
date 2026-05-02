import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Briefcase, RefreshCw, Save, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { assets } from "@/lib/mock-data";

export const Route = createFileRoute("/portfolio")({
  head: () => ({ meta: [{ title: "Portfolio — AI financial Portfolio" }, { name: "description", content: "Manage and rebalance your portfolio." }] }),
  component: PortfolioPage,
});

function PortfolioPage() {
  const [weights, setWeights] = useState<Record<string, number>>(
    Object.fromEntries(assets.map((a) => [a.symbol, a.allocation])),
  );
  const total = Object.values(weights).reduce((a, b) => a + b, 0);

  return (
    <AppShell>
      <PageHeader
        eyebrow="Portfolio"
        title="Asset Allocation"
        description="Drag sliders to adjust weights. AI-powered rebalancing keeps targets in sync."
        actions={
          <>
            <Button
              variant="outline"
              className="border-border bg-surface"
              onClick={() => toast.success("Draft saved", { description: "Your allocation changes are stored locally." })}
            >
              <Save className="mr-2 h-4 w-4" />Save Draft
            </Button>
            <Button
              className="bg-gradient-to-r from-primary to-info text-primary-foreground"
              onClick={() => {
                const reset = Object.fromEntries(assets.map((a) => [a.symbol, a.allocation]));
                setWeights(reset);
                toast.success("Portfolio rebalanced", { description: "Weights restored to AI target allocation." });
              }}
            >
              <RefreshCw className="mr-2 h-4 w-4" />Rebalance
            </Button>
          </>
        }
      />

      <div className="mb-6 grid gap-4 md:grid-cols-3">
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">Holdings</p>
          <p className="mt-1 font-display text-3xl font-bold">{assets.length}</p>
        </div>
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">Total Allocation</p>
          <p className={`mt-1 font-display text-3xl font-bold ${total === 100 ? "text-success" : "text-warning"}`}>{total}%</p>
        </div>
        <div className="glass-card rounded-2xl p-5">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">Drift from Target</p>
          <p className="mt-1 font-display text-3xl font-bold text-warning">+6.4%</p>
        </div>
      </div>

      <SectionCard title="Holdings" description="Editable allocation table" action={<Briefcase className="h-4 w-4 text-muted-foreground" />}>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border/60 text-left text-[11px] uppercase tracking-wider text-muted-foreground">
                <th className="px-2 pb-3 font-medium">Asset</th>
                <th className="px-2 pb-3 font-medium">Price</th>
                <th className="px-2 pb-3 font-medium">24h</th>
                <th className="px-2 pb-3 font-medium">Return</th>
                <th className="px-2 pb-3 font-medium">Risk</th>
                <th className="px-2 pb-3 font-medium min-w-[260px]">Allocation</th>
                <th className="px-2 pb-3 text-right font-medium">Weight</th>
              </tr>
            </thead>
            <tbody>
              {assets.map((a) => {
                const positive = a.change >= 0;
                const w = weights[a.symbol];
                return (
                  <tr key={a.symbol} className="border-b border-border/40 transition-colors hover:bg-surface/40">
                    <td className="px-2 py-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-primary/20 to-info/10 font-mono text-xs font-bold text-primary">
                          {a.symbol.slice(0, 2)}
                        </div>
                        <div>
                          <div className="text-sm font-semibold">{a.symbol}</div>
                          <div className="text-xs text-muted-foreground">{a.name}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-2 py-4 font-mono text-sm">${a.price.toLocaleString()}</td>
                    <td className="px-2 py-4">
                      <span className={`inline-flex items-center gap-1 font-mono text-sm font-semibold ${positive ? "text-success" : "text-destructive"}`}>
                        {positive ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
                        {positive ? "+" : ""}{a.change}%
                      </span>
                    </td>
                    <td className="px-2 py-4 font-mono text-sm text-success">+{a.return}%</td>
                    <td className="px-2 py-4">
                      <Badge variant="outline" className={
                        a.risk === "High" ? "border-destructive/30 bg-destructive/10 text-destructive" :
                        a.risk === "Medium" ? "border-warning/30 bg-warning/10 text-warning" :
                        "border-success/30 bg-success/10 text-success"
                      }>{a.risk}</Badge>
                    </td>
                    <td className="px-2 py-4">
                      <Slider
                        value={[w]}
                        max={50}
                        step={1}
                        onValueChange={(v) => setWeights({ ...weights, [a.symbol]: v[0] })}
                        className="w-full"
                      />
                    </td>
                    <td className="px-2 py-4 text-right">
                      <span className="font-mono text-sm font-bold tabular-nums">{w}%</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </SectionCard>
    </AppShell>
  );
}
