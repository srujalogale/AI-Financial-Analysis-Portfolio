import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { User, Mail, Phone, MapPin, Camera, Save, Shield, Key } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { PageHeader } from "@/components/ui-kit/PageHeader";
import { SectionCard } from "@/components/ui-kit/SectionCard";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/profile")({
  head: () => ({ meta: [{ title: "Profile — AI financial Portfolio" }, { name: "description", content: "Manage your account profile." }] }),
  component: ProfilePage,
});

function ProfilePage() {
  const [form, setForm] = useState({
    name: "Alex Rivera",
    email: "alex@aifinancialportfolio.ai",
    phone: "+1 (415) 555-0142",
    location: "San Francisco, CA",
    bio: "Long-term value investor focused on AI & semiconductors.",
  });

  const onSave = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success("Profile updated", { description: "Your changes have been saved." });
  };

  return (
    <AppShell>
      <PageHeader
        eyebrow="Account"
        title="Your Profile"
        description="Manage personal information and how others see you on AI financial Portfolio."
        actions={
          <Button onClick={onSave} className="bg-gradient-to-r from-primary to-info text-primary-foreground">
            <Save className="mr-2 h-4 w-4" />Save Changes
          </Button>
        }
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <SectionCard title="Profile Picture" description="JPG, PNG up to 2MB">
          <div className="flex flex-col items-center gap-4 py-2">
            <div className="relative">
              <Avatar className="h-28 w-28 ring-4 ring-primary/20">
                <AvatarFallback className="bg-gradient-to-br from-primary to-info text-2xl font-bold text-primary-foreground">
                  AR
                </AvatarFallback>
              </Avatar>
              <button
                onClick={() => toast.message("Upload", { description: "Photo upload coming soon." })}
                className="absolute -bottom-1 -right-1 flex h-9 w-9 items-center justify-center rounded-full border-2 border-background bg-primary text-primary-foreground shadow-lg transition-transform hover:scale-110"
              >
                <Camera className="h-4 w-4" />
              </button>
            </div>
            <div className="text-center">
              <p className="font-display text-lg font-bold">{form.name}</p>
              <Badge className="mt-1 border-primary/30 bg-primary/15 text-primary">Pro · Tier 3</Badge>
            </div>
            <div className="grid w-full grid-cols-3 gap-2 pt-2 text-center">
              <div className="rounded-lg border border-border bg-surface/60 p-2">
                <p className="font-display text-base font-bold">38</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Holdings</p>
              </div>
              <div className="rounded-lg border border-border bg-surface/60 p-2">
                <p className="font-display text-base font-bold text-success">+14%</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">YTD</p>
              </div>
              <div className="rounded-lg border border-border bg-surface/60 p-2">
                <p className="font-display text-base font-bold">2y</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Member</p>
              </div>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Personal Information" description="Update your details" className="lg:col-span-2">
          <form onSubmit={onSave} className="grid gap-4 md:grid-cols-2">
            <Field icon={<User className="h-4 w-4" />} label="Full Name" value={form.name} onChange={(v) => setForm({ ...form, name: v })} />
            <Field icon={<Mail className="h-4 w-4" />} label="Email" value={form.email} onChange={(v) => setForm({ ...form, email: v })} type="email" />
            <Field icon={<Phone className="h-4 w-4" />} label="Phone" value={form.phone} onChange={(v) => setForm({ ...form, phone: v })} />
            <Field icon={<MapPin className="h-4 w-4" />} label="Location" value={form.location} onChange={(v) => setForm({ ...form, location: v })} />
            <div className="md:col-span-2 space-y-1.5">
              <Label className="text-xs uppercase tracking-wider text-muted-foreground">Bio</Label>
              <textarea
                value={form.bio}
                onChange={(e) => setForm({ ...form, bio: e.target.value })}
                rows={3}
                className="w-full rounded-md border border-border/60 bg-surface px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </form>
        </SectionCard>
      </div>

      <SectionCard title="Security" description="Keep your account secure" className="mt-6">
        <div className="grid gap-3 md:grid-cols-2">
          <button
            onClick={() => toast.message("Change password", { description: "A reset link was sent to your email." })}
            className="flex items-center justify-between rounded-xl border border-border/60 bg-surface/60 p-4 text-left transition-all hover:border-primary/40"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/15 text-primary"><Key className="h-5 w-5" /></div>
              <div>
                <p className="text-sm font-semibold">Password</p>
                <p className="text-xs text-muted-foreground">Last changed 3 months ago</p>
              </div>
            </div>
            <span className="text-xs font-semibold text-primary">Change →</span>
          </button>
          <button
            onClick={() => toast.success("2FA enabled", { description: "Two-factor authentication is now active." })}
            className="flex items-center justify-between rounded-xl border border-border/60 bg-surface/60 p-4 text-left transition-all hover:border-primary/40"
          >
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-success/15 text-success"><Shield className="h-5 w-5" /></div>
              <div>
                <p className="text-sm font-semibold">Two-Factor Auth</p>
                <p className="text-xs text-muted-foreground">Authenticator app</p>
              </div>
            </div>
            <Badge className="border-success/30 bg-success/15 text-success">Active</Badge>
          </button>
        </div>
      </SectionCard>
    </AppShell>
  );
}

function Field({ icon, label, value, onChange, type = "text" }: { icon: React.ReactNode; label: string; value: string; onChange: (v: string) => void; type?: string }) {
  return (
    <div className="space-y-1.5">
      <Label className="text-xs uppercase tracking-wider text-muted-foreground">{label}</Label>
      <div className="relative">
        <div className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">{icon}</div>
        <Input type={type} value={value} onChange={(e) => onChange(e.target.value)} className="h-11 border-border/60 bg-surface pl-9" />
      </div>
    </div>
  );
}
