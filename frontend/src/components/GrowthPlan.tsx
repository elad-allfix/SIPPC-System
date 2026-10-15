import { useEffect, useState } from "react";
import { api } from "../api";
import type { GrowthPlan as Plan, GrowthPlanPart, Item } from "../types";
import Icon from "./Icon";
import { Markdown } from "./ui";

/** How each of the six parts looks, so a move reads as what it is before it is read. */
const PART: Record<string, { icon: string; short: string; tint: string; row: string }> = {
  keywords_add: { icon: "plus", short: "Keywords to add", tint: "bg-[#e7f4ee] text-[#1f8a5f]", row: "search" },
  keywords_cut: { icon: "minus", short: "Searches to cut", tint: "bg-[#fdecea] text-danger", row: "search" },
  bids_budgets: { icon: "money", short: "Bids and budgets", tint: "bg-accent-soft text-accent-ink", row: "plain" },
  settings: { icon: "sliders", short: "Settings", tint: "bg-sunken text-muted", row: "plain" },
  ads: { icon: "ad", short: "Ads", tint: "bg-[#e8f0fe] text-[#1a73e8]", row: "ad" },
  website: { icon: "page", short: "Website", tint: "bg-[#eef3fb] text-[#2d6fb8]", row: "page" },
};

/** Loads the plan and reloads it whenever the project's findings change. */
export function useGrowthPlan(projectId: string, version: string | undefined, enabled = true) {
  const [plan, setPlan] = useState<Plan | null>(null);
  useEffect(() => {
    if (!enabled) return;
    let alive = true;
    api.growthPlan(projectId).then((p) => { if (alive) setPlan(p); }).catch(() => { if (alive) setPlan(null); });
    return () => { alive = false; };
  }, [projectId, version, enabled]);
  return plan;
}

export function planDone(plan: Plan) {
  return plan.parts.length - plan.missing.length;
}

/** Six small segments, one per part, lit when the part has moves. */
export function PlanMeter({ plan, className = "" }: { plan: Plan; className?: string }) {
  return (
    <span className={`flex gap-1 ${className}`} aria-hidden="true">
      {plan.parts.map((p) => (
        <i key={p.key} title={p.title} className={`h-1.5 flex-1 rounded-full ${p.items.length ? "bg-accent shadow-[0_0_8px_rgba(224,148,34,.6)]" : "bg-current opacity-15"}`} />
      ))}
    </span>
  );
}

function Move({ item, look, onQuote }: { item: Item; look: string; onQuote: (i: Item) => void }) {
  const [open, setOpen] = useState(false);
  const shell = look === "search" ? "rounded-full border border-line bg-white px-3 py-1.5"
    : "rounded-xl bg-sunken px-3 py-2";
  return (
    <li className={open ? "rounded-xl bg-sunken px-3 py-2" : shell}>
      <button onClick={() => setOpen((o) => !o)} className="flex w-full items-start gap-2 text-left text-[13px] leading-snug" data-testid="plan-move">
        {look === "search" && <Icon name="search" className="mt-0.5 h-3.5 w-3.5 shrink-0 text-faint" />}
        {look === "page" && <span className="mt-1 flex shrink-0 gap-0.5">{[0, 1, 2].map((i) => <i key={i} className="h-1.5 w-1.5 rounded-full bg-[#c9c9c4]" />)}</span>}
        <span className="min-w-0 flex-1">
          {look === "ad" && <span className="mr-1.5 font-[Arial,Helvetica,sans-serif] text-[10px] font-bold text-[#202124]">Ad</span>}
          <span className={look === "ad" ? "text-[#1a0dab]" : ""}>{item.title}</span>
        </span>
      </button>
      {open && (
        <div className="mt-2 space-y-2 border-t border-line pt-2">
          <div className="text-[12.5px]"><Markdown>{item.body}</Markdown></div>
          <button onClick={() => onQuote(item)} className="text-[11px] font-semibold text-accent-ink hover:underline">Ask about this</button>
        </div>
      )}
    </li>
  );
}

function Part({ part, n, onQuote, onAsk }: { part: GrowthPlanPart; n: number; onQuote: (i: Item) => void; onAsk: (t: string) => void }) {
  const look = PART[part.key] ?? { icon: "chart", short: part.title, tint: "bg-sunken text-muted", row: "plain" };
  const empty = part.items.length === 0;
  return (
    <section data-testid="plan-part" data-part={part.key}
      className={`flex flex-col gap-2.5 rounded-[18px] p-4 ${empty ? "border border-dashed border-line" : "border border-line bg-panel"}`}>
      <header className="flex items-center gap-2.5" title={part.title}>
        <span className={`grid h-7 w-7 shrink-0 place-items-center rounded-lg ${empty ? "bg-sunken text-faint" : look.tint}`}>
          <Icon name={look.icon} className="h-[15px] w-[15px]" stroke={2.2} />
        </span>
        <span className={`min-w-0 flex-1 truncate text-[13px] font-semibold ${empty ? "text-faint" : ""}`}>
          <span className="mr-1.5 font-mono text-[10.5px] text-faint">{n}</span>{look.short}
        </span>
        {!empty && <span className="text-[11px] tabular-nums text-faint">{part.items.length}</span>}
      </header>
      {empty ? (
        <div className="flex items-center justify-between gap-2 text-[12px] text-faint">
          <span>Not yet.</span>
          <button onClick={() => onAsk(`Fill the growth plan part "${part.title}". `)} className="font-semibold text-accent-ink hover:underline">Ask for it</button>
        </div>
      ) : (
        <ul className="space-y-1.5">{part.items.map((i) => <Move key={i.id} item={i} look={look.row} onQuote={onQuote} />)}</ul>
      )}
    </section>
  );
}

/** The growth plan as six parts in a fixed order, each drawn like its subject; missing parts say "not yet". */
export default function GrowthPlanView({ plan, onQuote, onAsk }: { plan: Plan; onQuote: (i: Item) => void; onAsk: (t: string) => void }) {
  const done = planDone(plan);
  return (
    <div className="space-y-3" data-testid="growth-plan">
      <div className="rounded-2xl bg-frame px-4 py-3 text-frame-fg">
        <div className="flex items-center justify-between gap-3">
          <span className="flex items-center gap-2 text-[14px] font-semibold"><Icon name="target" className="h-4 w-4 text-[#f3b14b]" />Growth plan</span>
          <span className="text-xs tabular-nums text-frame-muted">{plan.complete ? "All 6 parts" : `${done} of ${plan.parts.length} parts`}</span>
        </div>
        <PlanMeter plan={plan} className="mt-2.5 text-frame-fg" />
      </div>
      <div className="gap-3 @2xl:columns-2 [&>*]:mb-3 [&>*]:break-inside-avoid">
        {plan.parts.map((p, i) => <Part key={p.key} part={p} n={i + 1} onQuote={onQuote} onAsk={onAsk} />)}
      </div>
    </div>
  );
}
