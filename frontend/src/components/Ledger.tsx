import type { Item } from "../types";

const VERDICTS = ["hit", "partial", "miss", "unscorable"] as const;
const today = () => new Date().toISOString().slice(0, 10);

/** Forecast ledger: what is due, and how past forecasts turned out. No hit rate until there are enough. */
type F = Item & { data: { review_after?: string; outcome?: { verdict?: string } } };

export default function Ledger({ items, onAsk }: { items: Item[]; onAsk: (text: string) => void }) {
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
          {due.map((f) => <div key={f.id} className="text-muted">· {f.title} <span className="text-faint">(after {f.data.review_after})</span></div>)}
          <button className="text-accent hover:underline" onClick={() => onAsk("Score the forecasts that are due for review.")}>Ask the strategist to score them</button>
        </div>
      )}
    </div>
  );
}
