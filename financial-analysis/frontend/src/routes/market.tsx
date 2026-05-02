import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Search, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { LineChart, Line, ResponsiveContainer } from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { market } from "@/lib/mock-data";

export const Route = createFileRoute("/market")({
  head: () => ({ meta: [{ title: "Market — AI financial Portfolio" }, { name: "description", content: "Real-time market prices and asset discovery." }] }),
  component: MarketPage,
});

function MarketPage() {
  const [q, setQ] = useState("");
  const [cat, setCat] = useState("All");
  const filtered = market.filter(
    (m) =>
      (cat === "All" || m.cat === cat) &&
      (m.symbol.toLowerCase().includes(q.toLowerCase()) || m.name.toLowerCase().includes(q.toLowerCase())),
  );

  return (
    <AppShell>
      <PageHeader eyebrow="Market" title="Live Markets" description="Real-time prices across stocks, ETFs, and crypto." />

      <div className="mb-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div className="relative max-w-sm flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search symbol or name…" className="h-10 border-border/60 bg-surface pl-9" />
        </div>
        <Tabs value={cat} onValueChange={setCat}>
          <TabsList className="bg-surface">
            {["All", "Stock", "ETF", "Crypto"].map((c) => (
              <TabsTrigger key={c} value={c} className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">{c}</TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {filtered.map((m) => {
          const positive = m.change >= 0;
          return (
            <button
              key={m.symbol}
              type="button"
              onClick={() => toast.message(`${m.symbol} · ${m.name}`, { description: `$${m.price.toLocaleString()} (${positive ? "+" : ""}${m.change}%)` })}
              className="glass-card group cursor-pointer rounded-2xl p-5 text-left transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-[var(--shadow-elevated)]">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-primary/20 to-info/10 font-mono text-xs font-bold text-primary">
                      {m.symbol.slice(0, 2)}
                    </div>
                    <div>
                      <p className="text-sm font-bold">{m.symbol}</p>
                      <p className="text-[11px] text-muted-foreground">{m.name}</p>
                    </div>
                  </div>
                </div>
                <span className="rounded-full border border-border/60 bg-surface px-2 py-0.5 text-[10px] uppercase tracking-wider text-muted-foreground">{m.cat}</span>
              </div>

              <div className="mt-4 flex items-end justify-between">
                <div>
                  <p className="font-display text-2xl font-bold tabular-nums">${m.price.toLocaleString()}</p>
                  <p className={`mt-1 inline-flex items-center gap-1 font-mono text-xs font-semibold ${positive ? "text-success" : "text-destructive"}`}>
                    {positive ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
                    {positive ? "+" : ""}{m.change}%
                  </p>
                </div>
                <div className="h-12 w-24">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={m.spark.map((v, i) => ({ i, v }))}>
                      <Line dataKey="v" stroke={positive ? "var(--chart-2)" : "var(--chart-5)"} strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </AppShell>
  );
}
