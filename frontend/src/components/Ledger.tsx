import { useEffect, useState } from "react";
import { api } from "../api";
import type { Item, Lesson } from "../types";

const VERDICTS = ["hit", "partial", "miss", "unscorable"] as const;
const today = () => new Date().toISOString().slice(0, 10);

/** Forecast ledger: what is due, and how past forecasts turned out. No hit rate until there are enough. */
type F = Item & { data: { review_after?: string; outcome?: { verdict?: string } } };

/** Record what happened to one forecast, in the user's own words, without asking the strategist. */
function Score({ f, onScored }: { f: F; onScored: () => void }) {
  const [open, setOpen] = useState(false);
  const [actual, setActual] = useState("");
  const [verdict, setVerdict] = useState<string>("hit");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const save = async () => {
    setSaving(true); setError(null);
    try { await api.scoreItem(f.id, { actual: actual.trim(), verdict }); setOpen(false); onScored(); }
    catch (e) { setError(String((e as Error).message ?? e)); }
    finally { setSaving(false); }
  };
  return (
    <div className="text-muted" data-testid="due-forecast">
      · {f.title} <span className="text-faint">(after {f.data.review_after})</span>
      {!open ? <button className="ml-1 text-accent hover:underline" onClick={() => setOpen(true)}>Record what happened</button> : (
        <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
          <input value={actual} onChange={(e) => setActual(e.target.value)} placeholder="What actually happened, e.g. 14 leads"
            className="min-w-0 flex-1 rounded-lg border border-line bg-sunken px-2 py-1 text-xs text-fg" data-testid="score-actual" />
          <select value={verdict} onChange={(e) => setVerdict(e.target.value)} className="rounded-lg border border-line bg-sunken px-2 py-1 text-xs text-fg">
            {VERDICTS.map((v) => <option key={v} value={v}>{v}</option>)}
          </select>
          <button disabled={!actual.trim() || saving} onClick={save} className="rounded-full bg-accent px-3 py-1 text-xs text-accent-fg disabled:opacity-50" data-testid="score-save">Save</button>
          <button onClick={() => setOpen(false)} className="text-xs text-faint hover:underline">Cancel</button>
          {error && <div className="w-full text-danger">{error}</div>}
        </div>
      )}
    </div>
  );
}

export default function Ledger({ items, onAsk, onScored }: { items: Item[]; onAsk: (text: string) => void; onScored: () => void }) {
  const forecasts = (items as F[]).filter((i) => i.kind === "forecast" && i.status !== "superseded" && i.status !== "dropped");
  if (forecasts.length === 0) return null;
  const scored = forecasts.filter((f) => f.data?.outcome?.verdict);
  const due = forecasts.filter((f) => !f.data?.outcome && f.status === "open" && f.data?.review_after && String(f.data.review_after) <= today());
  const counts = Object.fromEntries(VERDICTS.map((v) => [v, scored.filter((f) => f.data.outcome?.verdict === v).length]));
  const judged = counts.hit + counts.partial + counts.miss;
  return (
    <div className="space-y-2 rounded-xl border border-line bg-panel p-3 text-xs" data-testid="ledger">
      <div className="text-sm font-medium">Forecast ledger</div>
      <div className="text-muted">
        {forecasts.length} forecast{forecasts.length > 1 ? "s" : ""} · {scored.length} scored
        {scored.length > 0 && <> ({VERDICTS.filter((v) => counts[v]).map((v) => `${counts[v]} ${v}`).join(", ")})</>}
      </div>
      {judged >= 10
        ? <div className="text-muted">Hit rate {Math.round(((counts.hit + counts.partial / 2) / judged) * 100)}% of {judged} judged <span className="text-faint">[estimate]</span></div>
        : <div className="text-faint">A hit rate is shown once 10 forecasts have been judged.</div>}
      {due.length > 0 && (
        <div className="space-y-1 border-t border-line pt-2">
          <div className="font-medium text-amber-700 dark:text-amber-300">{due.length} due for review</div>
          {due.map((f) => <Score key={f.id} f={f} onScored={onScored} />)}
          <button className="text-accent hover:underline" onClick={() => onAsk("Score the forecasts that are due for review.")}>Or ask the strategist to score them from account data</button>
        </div>
      )}
    </div>
  );
}

/** What was learned: corrections the strategist recorded, for this project and shared ones. */
export function Lessons({ projectId, updatedAt }: { projectId: string; updatedAt: string }) {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  useEffect(() => { api.lessons(projectId).then(setLessons).catch(() => setLessons([])); }, [projectId, updatedAt]);
  if (lessons.length === 0) return null;
  return (
    <div className="space-y-2 rounded-xl border border-line bg-panel p-3 text-xs" data-testid="lessons">
      <div className="text-sm font-medium">Lessons · {lessons.length}</div>
      {lessons.map((l) => (
        <div key={l.id} className="space-y-0.5 border-t border-line pt-2 first-of-type:border-0 first-of-type:pt-0">
          <div className="text-faint line-through decoration-faint">{l.what_was_wrong}</div>
          <div className="text-muted">{l.correction}</div>
          <div className="text-faint">{l.project_id ? "This project" : "All projects"}{l.applies_to ? ` · ${l.applies_to}` : ""}</div>
        </div>
      ))}
    </div>
  );
}
