import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Bell, AlertTriangle, TrendingDown, RefreshCw, Info, BellRing } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { alerts as seedAlerts } from "@/lib/mock-data";

export const Route = createFileRoute("/alerts")({
  head: () => ({ meta: [{ title: "Alerts — AI financial Portfolio" }, { name: "description", content: "Risk and rebalance alerts." }] }),
  component: AlertsPage,
});

const iconFor = (t: string) => t === "risk" ? AlertTriangle : t === "drop" ? TrendingDown : t === "rebalance" ? RefreshCw : Info;

function AlertsPage() {
  const [alerts, setAlerts] = useState(seedAlerts);

  const dismiss = (id: string | number) => {
    setAlerts((prev) => prev.filter((a) => a.id !== id));
    toast.success("Alert dismissed");
  };

  return (
    <AppShell>
      <PageHeader
        eyebrow="Alerts"
        title="Notifications"
        description="Stay ahead of market events and portfolio changes."
        actions={
          <Button
            variant="outline"
            className="border-border bg-surface"
            onClick={() => toast.message("Alert rules", { description: "Notification preferences panel coming soon." })}
          >
            <BellRing className="mr-2 h-4 w-4" />Manage Rules
          </Button>
        }
      />

      {alerts.length === 0 && (
        <div className="glass-card flex flex-col items-center justify-center rounded-2xl py-16 text-center">
          <Bell className="h-10 w-10 text-muted-foreground/50" />
          <p className="mt-3 font-display text-lg font-semibold">All clear</p>
          <p className="mt-1 text-sm text-muted-foreground">No active alerts. We'll let you know when something needs attention.</p>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {alerts.map((a) => {
          const Icon = iconFor(a.type);
          const tone =
            a.severity === "high" ? { ring: "border-destructive/30", bg: "bg-destructive/10", text: "text-destructive", chip: "bg-destructive/15 text-destructive border-destructive/30" }
            : a.severity === "medium" ? { ring: "border-warning/30", bg: "bg-warning/10", text: "text-warning", chip: "bg-warning/15 text-warning border-warning/30" }
            : { ring: "border-info/30", bg: "bg-info/10", text: "text-info", chip: "bg-info/15 text-info border-info/30" };
          return (
            <div key={a.id} className={`glass-card relative overflow-hidden rounded-2xl p-5 transition-all hover:shadow-[var(--shadow-elevated)] ${tone.ring}`}>
              <div className={`pointer-events-none absolute -right-10 -top-10 h-28 w-28 rounded-full ${tone.bg} blur-2xl`} />
              <div className="relative flex items-start gap-3">
                <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${tone.bg} ${tone.text}`}>
                  <Icon className="h-5 w-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <Badge className={`border ${tone.chip} text-[10px] uppercase tracking-wider`}>{a.severity}</Badge>
                    <span className="font-mono text-[10px] uppercase text-muted-foreground">{a.time}</span>
                  </div>
                  <p className="mt-2 font-display text-base font-bold leading-snug">{a.title}</p>
                  <p className="mt-1 text-sm text-muted-foreground">{a.desc}</p>
                  <div className="mt-4 flex gap-2">
                    <Button
                      size="sm"
                      className="h-8 bg-gradient-to-r from-primary to-info text-primary-foreground"
                      onClick={() => toast.success("Action taken", { description: a.title })}
                    >
                      Take Action
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      className="h-8 text-muted-foreground"
                      onClick={() => dismiss(a.id)}
                    >
                      Dismiss
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </AppShell>
  );
}
