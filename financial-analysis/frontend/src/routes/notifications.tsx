import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Mail, Smartphone, MessageSquare, Save, Bell } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";

export const Route = createFileRoute("/notifications")({
  head: () => ({ meta: [{ title: "Notifications — AI financial Portfolio" }, { name: "description", content: "Notification preferences." }] }),
  component: NotificationsPage,
});

const categories = [
  { id: "price", label: "Price alerts", desc: "When an asset crosses a threshold" },
  { id: "rebalance", label: "Rebalance signals", desc: "AI-suggested portfolio rebalancing" },
  { id: "risk", label: "Risk events", desc: "Volatility spikes, drawdowns, VaR breaches" },
  { id: "news", label: "Market news", desc: "Breaking news that impacts your holdings" },
  { id: "ai", label: "AI insights", desc: "Daily personalized recommendations" },
  { id: "billing", label: "Billing & account", desc: "Invoices, renewals, security" },
];

const channels = [
  { id: "email", label: "Email", icon: Mail, hint: "alex@aifinancialportfolio.ai" },
  { id: "push", label: "Push", icon: Smartphone, hint: "iOS · macOS" },
  { id: "sms", label: "SMS", icon: MessageSquare, hint: "+1 (415) 555-0142" },
];

type Matrix = Record<string, Record<string, boolean>>;

function defaultMatrix(): Matrix {
  const m: Matrix = {};
  categories.forEach((c) => {
    m[c.id] = { email: true, push: c.id !== "news", sms: c.id === "risk" };
  });
  return m;
}

function NotificationsPage() {
  const [matrix, setMatrix] = useState<Matrix>(defaultMatrix());
  const [dnd, setDnd] = useState(false);
  const [dndStart, setDndStart] = useState("22:00");
  const [dndEnd, setDndEnd] = useState("07:00");
  const [digest, setDigest] = useState("daily");
  const [threshold, setThreshold] = useState([5]);
  const [sound, setSound] = useState(true);

  const toggle = (cat: string, ch: string) => {
    setMatrix((prev) => ({ ...prev, [cat]: { ...prev[cat], [ch]: !prev[cat][ch] } }));
  };

  const save = () => toast.success("Preferences saved", { description: "Your notification settings are updated." });
  const reset = () => { setMatrix(defaultMatrix()); toast.message("Reset to defaults"); };

  return (
    <AppShell>
      <PageHeader
        eyebrow="Notifications"
        title="Notification Preferences"
        description="Choose what you're notified about and how you receive alerts."
        actions={
          <>
            <Button variant="outline" className="border-border bg-surface" onClick={reset}>Reset</Button>
            <Button onClick={save} className="bg-gradient-to-r from-primary to-info text-primary-foreground">
              <Save className="mr-2 h-4 w-4" />Save Preferences
            </Button>
          </>
        }
      />

      <div className="grid gap-6 lg:grid-cols-3">
        {channels.map((ch) => {
          const enabledCount = categories.filter((c) => matrix[c.id][ch.id]).length;
          return (
            <div key={ch.id} className="glass-card rounded-2xl p-5">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary/15 text-primary">
                  <ch.icon className="h-5 w-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-display text-base font-bold">{ch.label}</p>
                  <p className="truncate text-xs text-muted-foreground">{ch.hint}</p>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between">
                <span className="text-xs text-muted-foreground">{enabledCount} / {categories.length} active</span>
                <span className="font-mono text-xs font-bold text-primary">{Math.round((enabledCount / categories.length) * 100)}%</span>
              </div>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-surface">
                <div className="h-full bg-gradient-to-r from-primary to-info transition-all" style={{ width: `${(enabledCount / categories.length) * 100}%` }} />
              </div>
            </div>
          );
        })}
      </div>

      <SectionCard title="Categories" description="Choose channels per notification type" className="mt-6">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border/60 text-left text-[11px] uppercase tracking-wider text-muted-foreground">
                <th className="px-2 pb-3 font-medium">Notification</th>
                {channels.map((ch) => (
                  <th key={ch.id} className="px-2 pb-3 text-center font-medium">{ch.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {categories.map((c) => (
                <tr key={c.id} className="border-b border-border/40">
                  <td className="px-2 py-4">
                    <p className="text-sm font-semibold">{c.label}</p>
                    <p className="text-xs text-muted-foreground">{c.desc}</p>
                  </td>
                  {channels.map((ch) => (
                    <td key={ch.id} className="px-2 py-4 text-center">
                      <div className="flex justify-center">
                        <Switch checked={matrix[c.id][ch.id]} onCheckedChange={() => toggle(c.id, ch.id)} />
                      </div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <SectionCard title="Quiet Hours" description="Pause non-critical notifications" action={<Bell className="h-4 w-4 text-muted-foreground" />}>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold">Do not disturb</p>
                <p className="text-xs text-muted-foreground">Mute notifications during set hours</p>
              </div>
              <Switch checked={dnd} onCheckedChange={setDnd} />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-xs uppercase tracking-wider text-muted-foreground">From</Label>
                <input
                  type="time" value={dndStart} onChange={(e) => setDndStart(e.target.value)} disabled={!dnd}
                  className="h-11 w-full rounded-md border border-border/60 bg-surface px-3 text-sm disabled:opacity-50"
                />
              </div>
              <div className="space-y-1.5">
                <Label className="text-xs uppercase tracking-wider text-muted-foreground">To</Label>
                <input
                  type="time" value={dndEnd} onChange={(e) => setDndEnd(e.target.value)} disabled={!dnd}
                  className="h-11 w-full rounded-md border border-border/60 bg-surface px-3 text-sm disabled:opacity-50"
                />
              </div>
            </div>
            <div className="flex items-center justify-between rounded-xl border border-border/60 bg-surface/60 p-3">
              <div>
                <p className="text-sm font-semibold">Notification sound</p>
                <p className="text-xs text-muted-foreground">Play sound for in-app alerts</p>
              </div>
              <Switch checked={sound} onCheckedChange={setSound} />
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Digest & Thresholds" description="Reduce noise, get the essentials">
          <div className="space-y-5">
            <div className="space-y-1.5">
              <Label className="text-xs uppercase tracking-wider text-muted-foreground">Email digest</Label>
              <Select value={digest} onValueChange={setDigest}>
                <SelectTrigger className="h-11 border-border/60 bg-surface"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="off">Off</SelectItem>
                  <SelectItem value="daily">Daily — 8:00 AM</SelectItem>
                  <SelectItem value="weekly">Weekly — Monday</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <div className="mb-2 flex justify-between text-xs">
                <span className="text-muted-foreground">Price alert threshold</span>
                <span className="font-mono font-semibold">±{threshold[0]}%</span>
              </div>
              <Slider value={threshold} onValueChange={setThreshold} min={1} max={20} step={1} />
              <p className="mt-2 text-xs text-muted-foreground">Notify when an asset moves by at least this percentage.</p>
            </div>

            <div className="rounded-xl border border-primary/20 bg-primary/5 p-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-primary">Tip</p>
              <p className="mt-1 text-xs text-muted-foreground">Critical risk alerts always bypass quiet hours and digest settings.</p>
            </div>
          </div>
        </SectionCard>
      </div>
    </AppShell>
  );
}
