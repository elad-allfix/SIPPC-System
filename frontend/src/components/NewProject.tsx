import { useState } from "react";
import type { EntryPath, ObjectiveType, Project } from "../types";
import { Button } from "./ui";

const PATHS: { v: EntryPath; title: string; help: string }[] = [
  { v: "new_niche", title: "New niche", help: "No website or campaigns yet. Research comes first." },
  { v: "website", title: "Website, no campaigns", help: "Research plus a review of the site." },
  { v: "ads_account", title: "Existing Ads account", help: "Account access needs Stage 01 (Phase 5). Research works now." },
];

const OBJECTIVES: ObjectiveType[] = ["profit", "leads", "sales", "traffic", "awareness", "unknown"];

const field = "w-full rounded-lg border border-line bg-panel px-3 py-2 text-sm outline-none focus:border-accent";

export default function NewProject({ onCreate, onCancel, canCancel }: {
  onCreate: (p: Partial<Project>) => Promise<void>; onCancel: () => void; canCancel: boolean;
}) {
  const [f, setF] = useState<Partial<Project>>({ entry_path: "new_niche", objective_type: "unknown" });
  const [err, setErr] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const set = (k: keyof Project, v: string) => setF((o) => ({ ...o, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!f.name?.trim()) { setErr("Give the project a name."); return; }
    setSaving(true); setErr(null);
    try {
      const clean = Object.fromEntries(Object.entries(f).map(([k, v]) => [k, typeof v === "string" && v.trim() === "" ? null : v]));
      await onCreate(clean as Partial<Project>);
    } catch (e) { setErr(String(e)); } finally { setSaving(false); }
  };

  return (
    <div className="fixed inset-0 z-40 grid place-items-center bg-black/30 p-4 backdrop-blur-[2px]">
      <form onSubmit={submit} className="w-full max-w-lg space-y-4 rounded-2xl border border-line bg-panel p-6 shadow-xl" data-testid="new-project">
        <div>
          <h2 className="text-lg font-semibold tracking-tight">New project</h2>
          <p className="text-sm text-muted">One business or niche. You can change all of this later in the conversation.</p>
        </div>
        <label className="block space-y-1"><span className="text-xs text-muted">Name</span>
          <input autoFocus className={field} value={f.name ?? ""} onChange={(e) => set("name", e.target.value)} placeholder="e.g. Emergency plumbing, Austin TX" name="name" /></label>
        <div className="space-y-1">
          <span className="text-xs text-muted">Starting point</span>
          <div className="grid gap-2">
            {PATHS.map((p) => (
              <label key={p.v} className={`flex cursor-pointer gap-3 rounded-lg border px-3 py-2 ${f.entry_path === p.v ? "border-accent bg-accent-soft" : "border-line"}`}>
                <input type="radio" name="entry_path" className="mt-1 accent-[var(--accent)]" checked={f.entry_path === p.v} onChange={() => set("entry_path", p.v)} />
                <span><span className="block text-sm font-medium">{p.title}</span><span className="block text-xs text-muted">{p.help}</span></span>
              </label>
            ))}
          </div>
        </div>
        <label className="block space-y-1"><span className="text-xs text-muted">Objective, in your words</span>
          <textarea rows={2} className={field} value={f.objective ?? ""} onChange={(e) => set("objective", e.target.value)} placeholder="e.g. Profitable booked jobs, around 40 a month" /></label>
        <div className="grid grid-cols-2 gap-3">
          <label className="block space-y-1"><span className="text-xs text-muted">Objective type</span>
            <select className={field} value={f.objective_type} onChange={(e) => set("objective_type", e.target.value)}>
              {OBJECTIVES.map((o) => <option key={o} value={o}>{o}</option>)}
            </select></label>
          <label className="block space-y-1"><span className="text-xs text-muted">Country</span>
            <input className={field} value={f.country ?? ""} onChange={(e) => set("country", e.target.value)} placeholder="e.g. United States" /></label>
          <label className="block space-y-1"><span className="text-xs text-muted">Region or city</span>
            <input className={field} value={f.region ?? ""} onChange={(e) => set("region", e.target.value)} placeholder="optional" /></label>
          <label className="block space-y-1"><span className="text-xs text-muted">Language</span>
            <input className={field} value={f.language ?? ""} onChange={(e) => set("language", e.target.value)} placeholder="e.g. English" /></label>
        </div>
        {f.entry_path !== "new_niche" && (
          <label className="block space-y-1"><span className="text-xs text-muted">Website</span>
            <input className={field} value={f.website_url ?? ""} onChange={(e) => set("website_url", e.target.value)} placeholder="https://" /></label>
        )}
        {err && <div className="text-sm text-danger">{err}</div>}
        <div className="flex justify-end gap-2 pt-1">
          {canCancel && <Button type="button" onClick={onCancel}>Cancel</Button>}
          <Button variant="primary" type="submit" disabled={saving}>{saving ? "Creating…" : "Create project"}</Button>
        </div>
      </form>
    </div>
  );
}
