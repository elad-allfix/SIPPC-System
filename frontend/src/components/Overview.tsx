import type { ProjectCard } from "../types";

const PATH: Record<string, string> = { new_niche: "New niche", website: "Website", ads_account: "Ads account" };
const GOAL: Record<string, string> = {
  profit: "Profit", leads: "Leads", sales: "Sales", traffic: "Traffic", awareness: "Awareness", unknown: "Goal not set",
};
const NEED: Record<string, { tag: string; color: string }> = {
  do: { tag: "Do", color: "var(--accent-ink)" },
  check: { tag: "Check", color: "var(--ev-estimate)" },
  answer: { tag: "Answer", color: "var(--ev-observed)" },
  fix: { tag: "Fix", color: "var(--danger)" },
  risk: { tag: "Risk", color: "var(--ev-unknown)" },
};

function ago(iso: string | null): string | null {
  if (!iso) return null;
  const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000);
  if (m < 60) return m <= 1 ? "just now" : `${m} min ago`;
  const h = Math.round(m / 60);
  if (h < 24) return `${h} h ago`;
  const d = Math.round(h / 24);
  return d === 1 ? "yesterday" : `${d} days ago`;
}

const plural = (n: number, one: string, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

/** All projects at a glance: what each one is, where it stands, and what it needs next. */
export default function Overview({ cards, loading, error, onOpen, onNew, onRetry }: {
  cards: ProjectCard[]; loading: boolean; error: string | null;
  onOpen: (id: string) => void; onNew: () => void; onRetry: () => void;
}) {
  return (
    <div className="sheet flex min-w-0 flex-1 flex-col" data-testid="overview">
      <div className="flex items-center gap-4 border-b border-line px-6 py-5">
        <div>
          <h1 className="text-2xl font-bold tracking-[-0.03em]">Projects</h1>
          <div className="text-sm text-faint">{loading ? "Loading…" : plural(cards.length, "project")}</div>
        </div>
        <button onClick={onNew} className="cta ml-auto !px-5 !py-2.5 !text-sm" data-testid="overview-new">+ New project</button>
      </div>
      <div className="min-h-0 flex-1 overflow-auto p-6 scroll-thin">
        {error ? (
          <div className="grid h-full place-items-center text-center" data-testid="overview-error">
            <div className="flex max-w-sm flex-col items-center gap-2">
              <b className="text-lg font-bold">Could not load the projects</b>
              <span className="text-sm text-muted">{error}</span>
              <button onClick={onRetry} className="mt-2 rounded-full border border-line px-4 py-2 text-sm hover:bg-sunken">Try again</button>
            </div>
          </div>
        ) : !loading && cards.length === 0 ? (
          <div className="grid h-full place-items-center text-center" data-testid="empty-dashboard">
            <div className="flex max-w-sm flex-col items-center gap-2">
              <b className="text-xl font-bold tracking-[-0.02em]">No projects yet</b>
              <span className="text-sm text-muted">A project holds one business: its research, plan, files and decisions.</span>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 2xl:grid-cols-3">
            {cards.map((c) => <Card key={c.id} c={c} onOpen={() => onOpen(c.id)} />)}
          </div>
        )}
      </div>
    </div>
  );
}

function Card({ c, onOpen }: { c: ProjectCard; onOpen: () => void }) {
  const place = [c.region, c.country].filter(Boolean).join(", ");
  const active = ago(c.last_activity);
  const stats = [
    plural(c.conversation_count, "conversation"),
    plural(c.item_total, "saved item"),
    c.file_count ? plural(c.file_count, "file") : null,
  ].filter(Boolean).join(" · ");
  return (
    <button onClick={onOpen} data-testid="project-card"
      className="group flex min-w-0 flex-col gap-4 rounded-2xl border border-line bg-panel p-5 text-left transition hover:-translate-y-0.5 hover:border-accent hover:shadow-[0_12px_40px_-18px_rgba(224,148,34,.55)]">
      <div className="flex flex-col gap-1.5">
        <div className="flex flex-wrap items-center gap-1.5 text-[11px] font-semibold uppercase tracking-[0.08em] text-faint">
          <span className="rounded-full bg-sunken px-2 py-0.5">{PATH[c.entry_path] ?? c.entry_path}</span>
          <span className="rounded-full bg-sunken px-2 py-0.5">{GOAL[c.objective_type] ?? c.objective_type}</span>
          {place && <span className="truncate normal-case tracking-normal">{place}</span>}
        </div>
        <b className="text-lg font-bold leading-snug tracking-[-0.02em] group-hover:text-accent-ink">{c.name}</b>
        {c.objective && <span className="line-clamp-2 text-sm text-muted">{c.objective}</span>}
      </div>

      <div className="flex items-center gap-3 text-xs text-faint">
        <span className="flex gap-1" title="Stages 1 to 7: filled where something is saved">
          {[1, 2, 3, 4, 5, 6, 7].map((n) => (
            <span key={n} className="h-1.5 w-4 rounded-full"
              style={{ background: c.stages_with_items.includes(n) ? "var(--accent)" : "var(--line)" }} />
          ))}
        </span>
        <span className="truncate">{stats}{active ? ` · active ${active}` : ""}</span>
      </div>

      {c.plan && (
        <div className="rounded-xl bg-accent-soft px-3.5 py-2.5 text-sm">
          <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-accent-ink">Current plan</div>
          <div className="line-clamp-2">{c.plan}</div>
        </div>
      )}

      <div className="flex flex-col gap-1.5" data-testid="needs">
        <div className="text-[11px] font-semibold uppercase tracking-[0.08em] text-faint">Needs</div>
        {c.needs.length ? c.needs.slice(0, 4).map((n, i) => (
          <div key={i} className="flex items-start gap-2 text-sm">
            <span className="mt-0.5 w-14 shrink-0 text-[11px] font-bold uppercase tracking-[0.06em]" style={{ color: NEED[n.kind]?.color }}>
              {NEED[n.kind]?.tag ?? n.kind}
            </span>
            <span className="line-clamp-2 min-w-0">{n.text}</span>
          </div>
        )).concat(c.needs.length > 4 ? [
          <span key="more" className="pl-16 text-xs text-faint">+{c.needs.length - 4} more inside</span>,
        ] : []) : (
          <span className="text-sm text-faint">
            {c.plan ? "Nothing else open." : c.item_total ? "Nothing open flagged yet." : "Nothing saved yet."}
          </span>
        )}
      </div>
    </button>
  );
}
