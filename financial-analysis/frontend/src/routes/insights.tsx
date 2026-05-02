import { createFileRoute } from "@tanstack/react-router";
import { toast } from "sonner";
import { Brain, TrendingUp, TrendingDown, Minus, ExternalLink } from "lucide-react";
import { RadialBarChart, RadialBar, ResponsiveContainer, PolarAngleAxis } from "recharts";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Badge } from "@/components/ui/badge";
import { news } from "@/lib/mock-data";

export const Route = createFileRoute("/insights")({
  head: () => ({ meta: [{ title: "Insights — AI financial Portfolio" }, { name: "description", content: "Market sentiment and AI-driven insights." }] }),
  component: InsightsPage,
});

function InsightsPage() {
  const overall = 0.42;
  const score = Math.round((overall + 1) * 50);

  return (
    <AppShell>
      <PageHeader eyebrow="AI Insights" title="Market Sentiment" description="NLP-powered analysis of news flow and impact on your portfolio." />

      <div className="mb-6 grid gap-6 lg:grid-cols-3">
        <SectionCard title="Overall Sentiment" description="Last 24h across 1,240 articles">
          <div className="relative h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart innerRadius="70%" outerRadius="100%" data={[{ name: "s", value: score, fill: "var(--chart-2)" }]} startAngle={180} endAngle={0}>
                <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
                <RadialBar background={{ fill: "var(--muted)" }} dataKey="value" cornerRadius={20} />
              </RadialBarChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <p className="font-display text-4xl font-bold text-success">+{(overall * 100).toFixed(0)}</p>
              <p className="text-xs uppercase tracking-wider text-muted-foreground">Bullish</p>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Topic Breakdown" description="Sentiment by sector" className="lg:col-span-2">
          <div className="space-y-3">
            {[
              { topic: "Technology", val: 0.72, articles: 412 },
              { topic: "Crypto", val: 0.58, articles: 184 },
              { topic: "Energy", val: -0.22, articles: 98 },
              { topic: "Financials", val: 0.18, articles: 156 },
              { topic: "Healthcare", val: 0.32, articles: 142 },
            ].map((t) => {
              const pct = (t.val + 1) * 50;
              const tone = t.val > 0.2 ? "bg-success" : t.val < -0.1 ? "bg-destructive" : "bg-warning";
              return (
                <div key={t.topic}>
                  <div className="mb-1.5 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold">{t.topic}</span>
                      <span className="text-muted-foreground">{t.articles} articles</span>
                    </div>
                    <span className={`font-mono font-semibold ${t.val > 0 ? "text-success" : "text-destructive"}`}>
                      {t.val > 0 ? "+" : ""}{(t.val * 100).toFixed(0)}
                    </span>
                  </div>
                  <div className="h-2 w-full overflow-hidden rounded-full bg-surface">
                    <div className={`h-full ${tone} transition-all`} style={{ width: `${pct}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="News Feed" description="Real-time, AI-scored" action={<Badge className="border-primary/30 bg-primary/15 text-primary"><Brain className="mr-1 h-3 w-3" />NLP v4</Badge>}>
        <div className="divide-y divide-border/40">
          {news.map((n) => {
            const Pos = n.sentiment > 0.2 ? TrendingUp : n.sentiment < -0.2 ? TrendingDown : Minus;
            const tone = n.sentiment > 0.2 ? "text-success bg-success/10" : n.sentiment < -0.2 ? "text-destructive bg-destructive/10" : "text-warning bg-warning/10";
            return (
              <button
                key={n.id}
                type="button"
                onClick={() => toast.message(n.title, { description: `${n.source} · Portfolio impact ${n.impact}` })}
                className="flex w-full items-start gap-4 py-4 text-left transition-colors hover:bg-surface/40 first:pt-0 last:pb-0"
              >
                <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${tone}`}>
                  <Pos className="h-5 w-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-primary">{n.source}</span>
                    <span className="text-[10px] text-muted-foreground">{n.time}</span>
                  </div>
                  <p className="mt-1 text-sm font-semibold leading-snug">{n.title}</p>
                  <div className="mt-2 flex flex-wrap items-center gap-2">
                    {n.tags.map((t) => (
                      <span key={t} className="rounded-full border border-border bg-surface px-2 py-0.5 text-[10px] text-muted-foreground">{t}</span>
                    ))}
                    <span className={`ml-auto font-mono text-xs font-bold ${n.impact.startsWith("+") ? "text-success" : "text-destructive"}`}>
                      Portfolio impact {n.impact}
                    </span>
                  </div>
                </div>
                <ExternalLink className="h-4 w-4 shrink-0 self-center text-muted-foreground" />
              </button>
            );
          })}
        </div>
      </SectionCard>
    </AppShell>
  );
}
