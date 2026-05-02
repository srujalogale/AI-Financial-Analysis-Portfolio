import { ReactNode } from "react";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: string;
  change?: number;
  icon?: ReactNode;
  hint?: string;
  tone?: "default" | "success" | "destructive" | "warning";
}

export function StatCard({ label, value, change, icon, hint, tone = "default" }: StatCardProps) {
  const positive = (change ?? 0) >= 0;
  const toneRing = {
    default: "from-primary/20 to-transparent",
    success: "from-success/25 to-transparent",
    destructive: "from-destructive/25 to-transparent",
    warning: "from-warning/25 to-transparent",
  }[tone];

  return (
    <div className="glass-card group relative overflow-hidden rounded-2xl p-5 transition-all hover:border-primary/30 hover:shadow-[var(--shadow-elevated)]">
      <div className={cn("pointer-events-none absolute -right-12 -top-12 h-32 w-32 rounded-full bg-gradient-to-br opacity-60 blur-2xl transition-opacity group-hover:opacity-100", toneRing)} />
      <div className="relative flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">{label}</p>
          <p className="font-display text-2xl font-bold tracking-tight md:text-3xl">{value}</p>
        </div>
        {icon && (
          <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-surface text-primary">
            {icon}
          </div>
        )}
      </div>
      <div className="relative mt-4 flex items-center justify-between text-xs">
        {change !== undefined ? (
          <span
            className={cn(
              "inline-flex items-center gap-1 rounded-full px-2 py-0.5 font-mono font-semibold",
              positive ? "bg-success/15 text-success" : "bg-destructive/15 text-destructive",
            )}
          >
            {positive ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
            {positive ? "+" : ""}
            {change.toFixed(2)}%
          </span>
        ) : <span />}
        {hint && <span className="text-muted-foreground">{hint}</span>}
      </div>
    </div>
  );
}
