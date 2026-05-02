import { createFileRoute } from "@tanstack/react-router";
import { toast } from "sonner";
import { CreditCard, Download, Check, Sparkles, Zap, Crown } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/billing")({
  head: () => ({ meta: [{ title: "Billing — AI financial Portfolio" }, { name: "description", content: "Manage subscription, invoices, and payment methods." }] }),
  component: BillingPage,
});

const plans = [
  { id: "starter", name: "Starter", price: 0, icon: Sparkles, features: ["5 portfolios", "Daily AI insights", "Email alerts"], current: false },
  { id: "pro", name: "Pro", price: 29, icon: Zap, features: ["Unlimited portfolios", "Real-time alerts", "Monte Carlo simulations", "Priority support"], current: true },
  { id: "enterprise", name: "Enterprise", price: 99, icon: Crown, features: ["Everything in Pro", "Custom strategies", "API access", "Dedicated advisor"], current: false },
];

const invoices = [
  { id: "INV-2026-04", date: "Apr 1, 2026", amount: 29, status: "Paid" },
  { id: "INV-2026-03", date: "Mar 1, 2026", amount: 29, status: "Paid" },
  { id: "INV-2026-02", date: "Feb 1, 2026", amount: 29, status: "Paid" },
  { id: "INV-2026-01", date: "Jan 1, 2026", amount: 29, status: "Paid" },
];

function BillingPage() {
  return (
    <AppShell>
      <PageHeader
        eyebrow="Billing"
        title="Subscription & Invoices"
        description="Manage your plan, payment method, and download invoices."
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <SectionCard title="Current Plan" description="Renews on May 1, 2026">
          <div className="rounded-2xl border border-primary/30 bg-gradient-to-br from-primary/15 to-info/5 p-5">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary/20 text-primary">
                <Zap className="h-5 w-5" />
              </div>
              <div>
                <p className="font-display text-2xl font-bold">Pro</p>
                <p className="text-xs text-muted-foreground">$29 / month</p>
              </div>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2 text-center">
              <div className="rounded-lg bg-background/40 p-2">
                <p className="font-display text-base font-bold">$87</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Spent (90d)</p>
              </div>
              <div className="rounded-lg bg-background/40 p-2">
                <p className="font-display text-base font-bold">29 days</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Until renewal</p>
              </div>
            </div>
            <Button
              variant="outline"
              className="mt-4 w-full border-border bg-background/60"
              onClick={() => toast.message("Cancel subscription", { description: "Your plan will remain active until May 1." })}
            >
              Cancel Subscription
            </Button>
          </div>
        </SectionCard>

        <SectionCard title="Payment Method" description="Default card on file" className="lg:col-span-2">
          <div className="rounded-2xl border border-border bg-gradient-to-br from-foreground/5 via-surface to-background p-5">
            <div className="flex items-start justify-between">
              <div>
                <Badge className="border-primary/30 bg-primary/15 text-primary">Default</Badge>
                <p className="mt-3 font-mono text-lg tracking-[0.2em]">•••• •••• •••• 4242</p>
                <p className="mt-1 text-xs text-muted-foreground">Visa · Expires 09/28</p>
              </div>
              <div className="flex h-10 w-14 items-center justify-center rounded-lg bg-primary/15 text-primary">
                <CreditCard className="h-5 w-5" />
              </div>
            </div>
          </div>
          <div className="mt-3 flex gap-2">
            <Button
              variant="outline"
              className="border-border bg-surface"
              onClick={() => toast.message("Add card", { description: "Payment method form will open here." })}
            >
              Add Card
            </Button>
            <Button
              variant="ghost"
              onClick={() => toast.success("Card updated", { description: "Default payment method changed." })}
            >
              Update
            </Button>
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Available Plans" description="Upgrade or downgrade anytime" className="mt-6">
        <div className="grid gap-4 md:grid-cols-3">
          {plans.map((p) => (
            <div
              key={p.id}
              className={`relative rounded-2xl border p-5 transition-all ${
                p.current ? "border-primary/40 bg-gradient-to-br from-primary/10 to-transparent shadow-[var(--shadow-glow)]" : "border-border/60 bg-surface/40 hover:border-primary/30"
              }`}
            >
              {p.current && <Badge className="absolute right-4 top-4 border-primary/30 bg-primary text-primary-foreground">Current</Badge>}
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/15 text-primary">
                <p.icon className="h-5 w-5" />
              </div>
              <p className="mt-3 font-display text-lg font-bold">{p.name}</p>
              <p className="mt-1">
                <span className="font-display text-3xl font-bold">${p.price}</span>
                <span className="text-xs text-muted-foreground">/mo</span>
              </p>
              <ul className="mt-4 space-y-2">
                {p.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-xs">
                    <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-success" />
                    <span className="text-muted-foreground">{f}</span>
                  </li>
                ))}
              </ul>
              <Button
                disabled={p.current}
                onClick={() => toast.success(`Switched to ${p.name}`, { description: "Plan change takes effect immediately." })}
                className={`mt-5 w-full ${p.current ? "" : "bg-gradient-to-r from-primary to-info text-primary-foreground"}`}
                variant={p.current ? "outline" : "default"}
              >
                {p.current ? "Current Plan" : `Switch to ${p.name}`}
              </Button>
            </div>
          ))}
        </div>
      </SectionCard>

      <SectionCard title="Invoice History" description="Download past invoices" className="mt-6">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border/60 text-left text-[11px] uppercase tracking-wider text-muted-foreground">
                <th className="px-2 pb-3 font-medium">Invoice</th>
                <th className="px-2 pb-3 font-medium">Date</th>
                <th className="px-2 pb-3 font-medium">Amount</th>
                <th className="px-2 pb-3 font-medium">Status</th>
                <th className="px-2 pb-3 text-right font-medium">Action</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((inv) => (
                <tr key={inv.id} className="border-b border-border/40 hover:bg-surface/40">
                  <td className="px-2 py-4 font-mono text-sm font-semibold">{inv.id}</td>
                  <td className="px-2 py-4 text-sm text-muted-foreground">{inv.date}</td>
                  <td className="px-2 py-4 font-mono text-sm">${inv.amount}.00</td>
                  <td className="px-2 py-4">
                    <Badge className="border-success/30 bg-success/15 text-success">{inv.status}</Badge>
                  </td>
                  <td className="px-2 py-4 text-right">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => toast.success("Downloading invoice", { description: `${inv.id}.pdf` })}
                    >
                      <Download className="mr-1.5 h-3.5 w-3.5" />PDF
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>
    </AppShell>
  );
}
