import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Globe, Palette, Lock, Trash2, Download, Bell } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select";

export const Route = createFileRoute("/settings")({
  head: () => ({ meta: [{ title: "Settings — AI financial Portfolio" }, { name: "description", content: "Account preferences and configuration." }] }),
  component: SettingsPage,
});

function SettingsPage() {
  const [lang, setLang] = useState("en-US");
  const [currency, setCurrency] = useState("USD");
  const [tz, setTz] = useState("America/Los_Angeles");
  const [theme, setTheme] = useState("light");
  const [reduceMotion, setReduceMotion] = useState(false);
  const [analytics, setAnalytics] = useState(true);
  const [publicProfile, setPublicProfile] = useState(false);

  return (
    <AppShell>
      <PageHeader
        eyebrow="Settings"
        title="Preferences"
        description="Customize your AI financial Portfolio experience and manage account data."
      />

      <div className="space-y-6">
        <SectionCard title="Regional" description="Language, currency, timezone" action={<Globe className="h-4 w-4 text-muted-foreground" />}>
          <div className="grid gap-4 md:grid-cols-3">
            <SelectField label="Language" value={lang} onChange={(v) => { setLang(v); toast.success("Language updated"); }} options={[
              { value: "en-US", label: "English (US)" },
              { value: "en-GB", label: "English (UK)" },
              { value: "es-ES", label: "Español" },
              { value: "fr-FR", label: "Français" },
              { value: "de-DE", label: "Deutsch" },
            ]} />
            <SelectField label="Currency" value={currency} onChange={(v) => { setCurrency(v); toast.success("Currency updated"); }} options={[
              { value: "USD", label: "USD — US Dollar" },
              { value: "EUR", label: "EUR — Euro" },
              { value: "GBP", label: "GBP — British Pound" },
              { value: "JPY", label: "JPY — Japanese Yen" },
              { value: "INR", label: "INR — Indian Rupee" },
            ]} />
            <SelectField label="Timezone" value={tz} onChange={(v) => { setTz(v); toast.success("Timezone updated"); }} options={[
              { value: "America/Los_Angeles", label: "Pacific (PT)" },
              { value: "America/New_York", label: "Eastern (ET)" },
              { value: "Europe/London", label: "London (GMT)" },
              { value: "Europe/Berlin", label: "Berlin (CET)" },
              { value: "Asia/Singapore", label: "Singapore (SGT)" },
            ]} />
          </div>
        </SectionCard>

        <SectionCard title="Appearance" description="Look and feel" action={<Palette className="h-4 w-4 text-muted-foreground" />}>
          <div className="space-y-4">
            <div>
              <Label className="text-xs uppercase tracking-wider text-muted-foreground">Theme</Label>
              <div className="mt-2 grid grid-cols-3 gap-2">
                {(["light", "dark", "system"] as const).map((t) => (
                  <button
                    key={t}
                    onClick={() => { setTheme(t); toast.success(`Theme: ${t}`); }}
                    className={`rounded-xl border p-3 text-sm font-semibold capitalize transition-all ${
                      theme === t ? "border-primary bg-primary/10 text-primary" : "border-border bg-surface hover:border-primary/40"
                    }`}
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
            <ToggleRow
              label="Reduce motion"
              desc="Minimize animations across the app"
              checked={reduceMotion}
              onChange={(v) => { setReduceMotion(v); toast.success(v ? "Reduced motion on" : "Reduced motion off"); }}
            />
          </div>
        </SectionCard>

        <SectionCard title="Privacy" description="Control your data" action={<Lock className="h-4 w-4 text-muted-foreground" />}>
          <div className="space-y-1">
            <ToggleRow
              label="Public profile"
              desc="Allow other users to view your profile"
              checked={publicProfile}
              onChange={(v) => { setPublicProfile(v); toast.success(v ? "Profile is public" : "Profile is private"); }}
            />
            <ToggleRow
              label="Usage analytics"
              desc="Help improve AI financial Portfolio by sharing anonymous usage data"
              checked={analytics}
              onChange={(v) => { setAnalytics(v); toast.success(v ? "Analytics on" : "Analytics off"); }}
            />
          </div>
        </SectionCard>

        <SectionCard title="Notifications" description="Email, push & in-app alerts" action={<Bell className="h-4 w-4 text-muted-foreground" />}>
          <div className="flex items-center justify-between rounded-xl border border-border/60 bg-surface/60 p-4">
            <div>
              <p className="text-sm font-semibold">Notification preferences</p>
              <p className="text-xs text-muted-foreground">Control alerts, digests, and channels</p>
            </div>
            <Button asChild variant="outline" className="border-border bg-surface">
              <Link to="/notifications">Manage →</Link>
            </Button>
          </div>
        </SectionCard>

        <SectionCard title="Data & Account" description="Export or delete your account">
          <div className="grid gap-3 md:grid-cols-2">
            <button
              onClick={() => toast.success("Export started", { description: "We'll email you a link when ready." })}
              className="flex items-center justify-between rounded-xl border border-border/60 bg-surface/60 p-4 text-left transition-all hover:border-primary/40"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-info/15 text-info"><Download className="h-5 w-5" /></div>
                <div>
                  <p className="text-sm font-semibold">Export data</p>
                  <p className="text-xs text-muted-foreground">Download all your portfolios as JSON</p>
                </div>
              </div>
            </button>
            <button
              onClick={() => toast.error("Delete account", { description: "This action requires email confirmation." })}
              className="flex items-center justify-between rounded-xl border border-destructive/30 bg-destructive/5 p-4 text-left transition-all hover:bg-destructive/10"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-destructive/15 text-destructive"><Trash2 className="h-5 w-5" /></div>
                <div>
                  <p className="text-sm font-semibold text-destructive">Delete account</p>
                  <p className="text-xs text-muted-foreground">Permanently remove your data</p>
                </div>
              </div>
            </button>
          </div>
        </SectionCard>
      </div>
    </AppShell>
  );
}

function ToggleRow({ label, desc, checked, onChange }: { label: string; desc: string; checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-border/40 py-3 last:border-0">
      <div>
        <p className="text-sm font-semibold">{label}</p>
        <p className="text-xs text-muted-foreground">{desc}</p>
      </div>
      <Switch checked={checked} onCheckedChange={onChange} />
    </div>
  );
}

function SelectField({ label, value, onChange, options }: { label: string; value: string; onChange: (v: string) => void; options: { value: string; label: string }[] }) {
  return (
    <div className="space-y-1.5">
      <Label className="text-xs uppercase tracking-wider text-muted-foreground">{label}</Label>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="h-11 border-border/60 bg-surface"><SelectValue /></SelectTrigger>
        <SelectContent>
          {options.map((o) => <SelectItem key={o.value} value={o.value}>{o.label}</SelectItem>)}
        </SelectContent>
      </Select>
    </div>
  );
}
