import type { ProjectCard } from "../types";
import { Orbits } from "./Ignition";

const PATH: Record<string, string> = { new_niche: "New niche", website: "Website", ads_account: "Ads account" };
const GOAL: Record<string, string> = {
  profit: "Profit", leads: "Leads", sales: "Sales", traffic: "Traffic", awareness: "Awareness", unknown: "Goal not set",
};
const STAGE = ["Connection", "Business", "Market", "Website & ads", "Growth", "Learning", "Control"];
type Kind = ProjectCard["needs"][number]["kind"];
const NEED: Record<Kind, { tag: string; color: string }> = {
  fix: { tag: "Fix", color: "#e2553a" },
  risk: { tag: "Risk", color: "#d94a6a" },
  do: { tag: "Do", color: "#e09422" },
  check: { tag: "Check", color: "#9a7ce0" },
  answer: { tag: "Answer", color: "#4f8fe0" },
};
const RANK: Record<Kind, number> = { fix: 0, risk: 1, do: 2, check: 3, answer: 4 };

const isTest = (c: ProjectCard) => /\(test run\)\s*$/i.test(c.name);
const shortName = (c: ProjectCard) => c.name.replace(/\s*\(test run\)\s*$/i, "");
const ranked = (c: ProjectCard) => [...c.needs].sort((a, b) => RANK[a.kind] - RANK[b.kind]);
/** Who needs the user first: real projects before test runs, then the most severe need, then the most needs. */
const urgency = (c: ProjectCard) => {
  const top = ranked(c)[0];
  return [isTest(c) ? 1 : 0, top ? RANK[top.kind] : 9, -c.needs.length] as const;
};
const byUrgency = (a: ProjectCard, b: ProjectCard) => {
  const x = urgency(a), y = urgency(b);
  return x[0] - y[0] || x[1] - y[1] || x[2] - y[2];
};

function Dot({ kind }: { kind: Kind }) {
  const c = NEED[kind]?.color ?? "var(--faint)";
  return <span className="mt-[0.4em] inline-block h-2 w-2 shrink-0 rounded-full" style={{ background: c, boxShadow: `0 0 10px ${c}` }} />;
}

/** All projects at a glance: who needs the user first, then one card per project with its most urgent need. */
export default function Overview({ cards, loading, error, onOpen, onNew, onRetry }: {
  cards: ProjectCard[]; loading: boolean; error: string | null;
  onOpen: (id: string) => void; onNew: () => void; onRetry: () => void;
}) {
  const sorted = [...cards].sort(byUrgency);
  const first = sorted.find((c) => c.needs.length > 0);
  const all = cards.flatMap((c) => c.needs);
  const fixOrRisk = all.filter((n) => n.kind === "fix" || n.kind === "risk").length;
  const answers = all.filter((n) => n.kind === "answer").length;
  return (
    <div className="relative min-w-0 flex-1 overflow-hidden rounded-[22px] border border-line bg-[#0d0e11]" data-testid="overview">
      <Orbits dim />
      <div className="relative h-full overflow-auto px-6 pb-8 pt-7 scroll-thin max-sm:px-3">
        <div className="mb-6 flex flex-wrap items-center gap-x-9 gap-y-4">
          <div className="max-w-[24ch] text-[clamp(22px,3.2vw,34px)] font-bold leading-[1.15] tracking-[-0.035em]" data-testid="verdict">
            {loading ? "Loading your projects…" : error ? "Could not load the projects."
              : cards.length === 0 ? "No projects yet."
              : first ? <><em className="not-italic text-accent [text-shadow:0_0_24px_rgba(224,148,34,.55)]">{shortName(first)}</em> needs you first.</>
              : "Nothing needs you right now."}
            {first && !loading && !error && (
              <div className="mt-2 text-sm font-normal leading-snug tracking-normal text-faint">{ranked(first)[0].text}</div>
            )}
          </div>
          <div className="ml-auto flex flex-wrap items-end gap-7 max-md:ml-0">
            <Kpi n={cards.length} label="Projects" />
            <Kpi n={fixOrRisk} label="Fix or risk" kind="fix" />
            <Kpi n={answers} label="Your answers" kind="answer" />
            <button onClick={onNew} className="cta !px-5 !py-2.5 !text-sm" data-testid="overview-new">+ New project</button>
          </div>
        </div>

        {error ? (
          <div className="flex flex-col items-start gap-2 text-sm text-faint" data-testid="overview-error">
            <span>{error}</span>
            <button onClick={onRetry} className="rounded-full border border-line px-4 py-2 text-fg hover:bg-panel">Try again</button>
          </div>
        ) : !loading && cards.length === 0 ? (
          <div className="text-sm text-faint" data-testid="empty-dashboard">A project holds one business: its research, plan, files and decisions. Start one with New project.</div>
        ) : (
          <div className="grid grid-cols-[repeat(auto-fill,minmax(270px,1fr))] gap-3.5 max-sm:grid-cols-1">
            {sorted.map((c) => <Card key={c.id} c={c} hot={c.id === first?.id} onOpen={() => onOpen(c.id)} />)}
          </div>
        )}
      </div>
    </div>
  );
}

function Kpi({ n, label, kind }: { n: number; label: string; kind?: Kind }) {
  return (
    <div className="flex flex-col gap-1">
      <b className="text-[30px] font-light tabular-nums tracking-[-0.03em]">{n}</b>
      <span className="flex items-center gap-1.5 text-[11px] uppercase tracking-[0.08em] text-faint">
        {kind && <Dot kind={kind} />}{label}
      </span>
    </div>
  );
}

function Card({ c, hot, onOpen }: { c: ProjectCard; hot: boolean; onOpen: () => void }) {
  const needs = ranked(c);
  const top = needs[0];
  const last = Math.max(0, ...c.stages_with_items);
  const place = [c.region, c.country].filter(Boolean).join(", ");
  return (
    <button onClick={onOpen} data-testid="project-card" data-hot={hot || undefined}
      className={`flex min-w-0 flex-col gap-4 rounded-[22px] border bg-[linear-gradient(180deg,rgba(32,34,40,.92),rgba(23,24,29,.92))] p-5 text-left backdrop-blur-sm transition hover:-translate-y-0.5 ${
        hot ? "border-accent/75 shadow-[0_0_0_5px_rgba(224,148,34,.16),0_0_50px_-10px_rgba(224,148,34,.55)]" : "border-line hover:border-accent/60"}`}>
      <div className="flex items-start justify-between gap-2.5">
        <div className="min-w-0">
          <div className="text-[17px] font-bold leading-snug tracking-[-0.025em]">{shortName(c)}</div>
          <div className="mt-1 flex flex-wrap items-center gap-1.5 text-xs text-faint">
            {place && <span>{place}</span>}
            {isTest(c) && <span className="rounded-full bg-[#202228] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em]">Test</span>}
          </div>
        </div>
        <div title="Open needs" className={`grid h-[46px] w-[46px] shrink-0 place-items-center rounded-full border text-base font-bold tabular-nums ${
          hot ? "border-transparent bg-accent text-accent-fg shadow-[0_0_22px_rgba(224,148,34,.55)]" : "border-line"}`}>{c.needs.length}</div>
      </div>

      <div>
        <div className="flex items-center gap-[5px]" title="Stages 1 to 7: lit where something is saved">
          {STAGE.map((_, k) => (
            <i key={k} className={`h-1 flex-1 rounded-full ${c.stages_with_items.includes(k + 1) ? "bg-accent" : "bg-line"}`}
              style={k + 1 === last ? { boxShadow: "0 0 10px rgba(224,148,34,.55)" } : undefined} />
          ))}
        </div>
        <div className="mt-1.5 flex justify-between gap-2 text-[11px] text-[#5d6069]">
          <span>{PATH[c.entry_path] ?? c.entry_path} · {GOAL[c.objective_type] ?? c.objective_type}</span>
          <span>{last ? STAGE[last - 1] : "Nothing saved yet"}</span>
        </div>
      </div>

      <div className="flex gap-2.5 text-sm font-medium leading-snug" data-testid="needs">
        {top ? <><Dot kind={top.kind} /><span className="line-clamp-3">{top.text}</span></>
          : <span className="text-faint">{c.item_total ? "Nothing open needs you." : "Nothing saved yet."}</span>}
      </div>
      {needs.length > 1 && (
        <div className="flex flex-wrap gap-1.5">
          {needs.slice(1).map((n, i) => (
            <span key={i} className="flex items-center gap-1.5 rounded-full bg-[#202228] px-2.5 py-1 text-[11.5px] text-faint">
              <span className="h-1.5 w-1.5 rounded-full" style={{ background: NEED[n.kind]?.color }} />{NEED[n.kind]?.tag ?? n.kind}
            </span>
          ))}
        </div>
      )}

      <div className="mt-auto border-t border-line pt-3 text-xs leading-relaxed text-faint">
        <b className="mb-0.5 block text-[10px] font-semibold uppercase tracking-[0.08em] text-accent">Plan</b>
        <span className="line-clamp-3">{c.plan ?? "Not set yet"}</span>
      </div>
    </button>
  );
}
