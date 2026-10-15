import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { Project, ProjectCard } from "../types";
import { DeleteProject } from "./DeleteProject";
import { Orbits } from "./Ignition";
import { PlanMeter, planDone, useGrowthPlan } from "./GrowthPlan";

type Finding = ProjectCard["findings"][number];
type Missing = ProjectCard["missing"][number];

/** The Ember look: a light, warm page with the entrance page's finish (mono eyebrow, big headline with the
 *  amber dot, orbits, glow) and dark cards with an amber hairline. */
const PAGE_BG = "radial-gradient(900px 520px at 88% -8%, rgba(224,148,34,.20), transparent 62%), radial-gradient(700px 420px at 0% 110%, rgba(224,148,34,.08), transparent 60%), #ebe8e1";
const CARD_SHELL = "rounded-[24px] bg-[linear-gradient(180deg,#1d1e23,#121317)] ring-1 ring-white/[.06] shadow-[0_30px_60px_-32px_rgba(40,24,0,.75)] hover:shadow-[0_0_0_6px_rgba(224,148,34,.14),0_0_44px_rgba(224,148,34,.38),0_30px_60px_-32px_rgba(40,24,0,.75)]";
const today = () => new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });

const TONE = { red: "#e2553a", amber: "#e09422", blue: "#4f8fe0" };
const findingTone = (f: Finding) => (f.kind === "finding" ? TONE.amber : TONE.red);
const missingText = (m: Missing) => (m.kind === "check" ? `Result needed: ${m.text}` : m.text);

const isTest = (c: ProjectCard) => /\(test run\)\s*$/i.test(c.name);
const shortName = (c: ProjectCard) => c.name.replace(/\s*\(test run\)\s*$/i, "");
/** Real projects first, then the most recently active. */
const order = (a: ProjectCard, b: ProjectCard) =>
  Number(isTest(a)) - Number(isTest(b)) || String(b.last_activity ?? "").localeCompare(String(a.last_activity ?? ""));

/** All projects at a glance: for each, what was found and what is missing from the owner. */
export default function Overview({ cards, loading, error, onOpen, onNew, onRetry, onEdit, onChanged }: {
  cards: ProjectCard[]; loading: boolean; error: string | null;
  onOpen: (id: string) => void; onNew: () => void; onRetry: () => void;
  onEdit: (id: string, patch: Partial<Project>) => Promise<void>;
  /** Projects were moved in or out of the bin, or deleted: reload the lists. */
  onChanged: () => void;
}) {
  const deleteProject = async (c: ProjectCard) => { await api.trashProject(c.id); onChanged(); };
  const sorted = [...cards].sort(order);
  const findings = cards.reduce((n, c) => n + (c.findings?.length ?? 0), 0);
  const missing = cards.reduce((n, c) => n + (c.missing?.length ?? 0), 0);
  const summary = loading ? "Loading…" : error ? "Could not load the projects."
    : cards.length === 0 ? "No projects yet." : `${findings} findings to read, ${missing} things only you can give.`;

  return (
    <div className="sheet relative min-w-0 flex-1 overflow-hidden rounded-[22px]" style={{ background: PAGE_BG }} data-testid="overview">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[520px] opacity-90"><Orbits /></div>
      <div className="relative flex h-full flex-col overflow-y-auto pb-8 pt-10 scroll-thin">
        <div className="mb-10 flex flex-wrap items-end gap-x-10 gap-y-6 px-8 max-sm:px-4" data-testid="verdict">
          <div className="flex min-w-0 flex-col gap-3">
            <div className="font-mono text-[11px] uppercase tracking-[0.32em] text-faint">AllFix · Projects · {today()}</div>
            <h1 className="text-[clamp(40px,5.4vw,68px)] font-extrabold leading-[0.95] tracking-[-0.045em]">
              Your projects<span className="text-accent">.</span>
            </h1>
            <div className="text-[15px] text-faint">{summary}</div>
          </div>
          <div className="ml-auto flex flex-wrap items-end gap-8 max-md:ml-0">
            <Kpi n={cards.length} label="Projects" />
            <Kpi n={findings} label="Findings" tone={TONE.amber} />
            <Kpi n={missing} label="From you" tone={TONE.blue} />
          </div>
          <div className="max-md:w-full">
            <button onClick={onNew} className="cta !px-5 !py-2.5 !text-sm" data-testid="overview-new">+ New project</button>
          </div>
        </div>

        {error ? (
          <div className="flex flex-col items-start gap-2 px-8 text-sm text-faint" data-testid="overview-error">
            <span>{error}</span>
            <button onClick={onRetry} className="rounded-full border border-line px-4 py-2 text-fg hover:bg-panel">Try again</button>
          </div>
        ) : !loading && cards.length === 0 ? (
          <div className="px-8 text-sm text-faint" data-testid="empty-dashboard">A project holds one business: its research, plan, files and decisions. Start one with New project.</div>
        ) : (
          <Carousel count={sorted.length}>
            {sorted.map((c, i) => <Card key={c.id} c={c} n={i + 1} onOpen={() => onOpen(c.id)}
              onEdit={(patch) => onEdit(c.id, patch)} onTrash={() => deleteProject(c)} />)}
          </Carousel>
        )}
      </div>
    </div>
  );
}

/** One row of cards that scrolls sideways: snaps to a card, arrows on the edges, the edges fade where more
 *  cards wait, and a thin amber track shows where you are. Trackpad, touch, arrows and the keyboard all move it. */
function Carousel({ count, children }: { count: number; children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const [pos, setPos] = useState({ left: false, right: false, start: 0, size: 1 });
  const measure = () => {
    const el = ref.current;
    if (!el) return;
    const max = el.scrollWidth - el.clientWidth;
    setPos({ left: el.scrollLeft > 4, right: el.scrollLeft < max - 4,
      start: el.scrollWidth ? el.scrollLeft / el.scrollWidth : 0, size: el.scrollWidth ? el.clientWidth / el.scrollWidth : 1 });
  };
  useEffect(() => {
    measure();
    const el = ref.current;
    if (!el) return;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, [count]);
  const step = (dir: 1 | -1) => {
    const el = ref.current;
    if (!el) return;
    const card = el.querySelector<HTMLElement>("[data-testid=project-card]");
    const by = card ? card.offsetWidth + 20 : el.clientWidth * 0.8;
    el.scrollBy({ left: dir * Math.max(by, Math.floor(el.clientWidth / by) * by), behavior: "smooth" });
  };
  const fade = `linear-gradient(90deg, ${pos.left ? "transparent 0, #000 40px" : "#000 0"}, ${pos.right ? "#000 calc(100% - 40px), transparent 100%" : "#000 100%"})`;
  const arrow = (dir: 1 | -1, show: boolean) => (
    <button onClick={() => step(dir)} aria-label={dir < 0 ? "Previous projects" : "Next projects"} data-testid={dir < 0 ? "carousel-prev" : "carousel-next"}
      className={`absolute top-1/2 z-10 grid h-12 w-12 -translate-y-1/2 place-items-center rounded-full bg-[#17181c] text-lg text-[#ecebe8] ring-1 ring-white/10 transition duration-300 hover:bg-accent hover:text-accent-fg hover:shadow-[0_0_0_6px_rgba(224,148,34,.16),0_0_32px_rgba(224,148,34,.5)] max-sm:hidden ${
        dir < 0 ? "left-3" : "right-3"} ${show ? "opacity-100" : "pointer-events-none opacity-0"}`}>
      {dir < 0 ? "←" : "→"}
    </button>
  );
  return (
    <div className="relative" data-testid="carousel">
      {arrow(-1, pos.left)}
      <div ref={ref} onScroll={measure} tabIndex={0} aria-label="Projects"
        onKeyDown={(e) => { if (e.target !== e.currentTarget) return; if (e.key === "ArrowRight") step(1); if (e.key === "ArrowLeft") step(-1); }}
        className="flex snap-x snap-mandatory items-stretch gap-5 -my-4 overflow-x-auto scroll-smooth px-8 pb-16 pt-6 outline-none [scrollbar-width:none] max-sm:gap-3 max-sm:px-4 [&::-webkit-scrollbar]:hidden"
        style={{ WebkitMaskImage: fade, maskImage: fade, scrollPaddingInline: "2rem" }}>
        {children}
      </div>
      {arrow(1, pos.right)}
      {pos.size < 0.999 && (
        <div className="mx-auto -mt-6 h-1 w-40 overflow-hidden rounded-full bg-black/10" aria-hidden data-testid="carousel-track">
          <div className="h-full rounded-full bg-accent shadow-[0_0_10px_rgba(224,148,34,.7)] transition-[margin] duration-150"
            style={{ width: `${pos.size * 100}%`, marginLeft: `${pos.start * 100}%` }} />
        </div>
      )}
    </div>
  );
}

function Kpi({ n, label, tone }: { n: number; label: string; tone?: string }) {
  return (
    <div className="flex flex-col gap-1">
      <b className="text-[44px] font-light leading-none tabular-nums tracking-[-0.03em]">{n}</b>
      <span className="flex items-center gap-1.5 font-mono text-[10.5px] uppercase tracking-[0.22em] text-faint">
        {tone && <span className="h-2 w-2 rounded-full" style={{ background: tone }} />}{label}
      </span>
    </div>
  );
}

function Card({ c, n, onOpen, onEdit, onTrash }: {
  c: ProjectCard; n: number; onOpen: () => void;
  onEdit: (patch: Partial<Project>) => Promise<void>; onTrash: () => Promise<void>;
}) {
  const num = String(n).padStart(2, "0");
  return (
    <div role="button" tabIndex={0} onClick={onOpen} onKeyDown={(e) => { if (e.key === "Enter" && e.target === e.currentTarget) onOpen(); }}
      data-testid="project-card"
      className={`frame group relative flex w-[340px] shrink-0 snap-start cursor-pointer flex-col gap-4 p-5 text-left text-fg transition duration-300 hover:-translate-y-0.5 max-sm:w-[84vw] ${CARD_SHELL}`}>
      <span aria-hidden className="pointer-events-none absolute inset-x-6 top-0 h-px bg-[linear-gradient(90deg,transparent,rgba(224,148,34,.9),transparent)]" />
      <div>
        <div className="mb-2 font-mono text-[11px] tracking-[0.1em] text-accent">{num}</div>
        <Head c={c} onEdit={onEdit} onTrash={onTrash} />
      </div>
      <Panels c={c} />
      <PlanLine projectId={c.id} version={c.last_activity ?? undefined} />
    </div>
  );
}

/** "Growth plan: 4 of 6 parts" with one lit segment per part that has moves. */
function PlanLine({ projectId, version }: { projectId: string; version?: string }) {
  const plan = useGrowthPlan(projectId, version);
  if (!plan) return null;
  return (
    <div className="-mt-1 text-xs text-faint" data-testid="card-plan" title={plan.missing.length
      ? `Still missing: ${plan.parts.filter((p) => !p.items.length).map((p) => p.title).join("; ")}` : "All six parts are in"}>
      <div className="mb-1.5 flex items-center justify-between">
        <span className="font-mono text-[10.5px] uppercase tracking-[0.18em] text-accent">Growth plan</span>
        <span className="tabular-nums">{plan.complete ? "complete" : `${planDone(plan)} of ${plan.parts.length} parts`}</span>
      </div>
      <PlanMeter plan={plan} className="text-fg" />
    </div>
  );
}

const emptyFound = (c: ProjectCard) => (c.item_total ? "Nothing important found yet." : "Nothing researched yet.");
const SHOWN = 2;

/** Findings in a warm glass panel, asks in a cool one, each with a glowing count; then the plan. */
function Panels({ c }: { c: ProjectCard }) {
  const findings = c.findings ?? [], missing = c.missing ?? [];
  const panel = (title: string, count: number, tone: string, testid: string, empty: string, rows: React.ReactNode) => (
    <div data-testid={testid} className="rounded-[16px] p-3.5"
      style={{ background: `linear-gradient(180deg, ${tone}1f, ${tone}0a)`, boxShadow: `inset 0 0 0 1px ${tone}33` }}>
      <div className="mb-2.5 flex items-center justify-between">
        <span className="font-mono text-[10.5px] uppercase tracking-[0.18em]" style={{ color: tone }}>{title}</span>
        <span className="grid h-6 min-w-6 place-items-center rounded-full px-1.5 text-[11px] font-bold tabular-nums text-[#111]"
          style={{ background: tone, boxShadow: `0 0 14px ${tone}99`, opacity: count ? 1 : 0.35 }}>{count}</span>
      </div>
      {count === 0 ? <div className="text-[13px] text-faint">{empty}</div> : (
        <ul className="flex flex-col gap-2">
          {rows}
          {count > SHOWN && <li className="pl-4 text-xs text-faint">+{count - SHOWN} more inside</li>}
        </ul>
      )}
    </div>
  );
  return (
    <>
      {panel("Found", findings.length, TONE.amber, "findings", emptyFound(c),
        findings.slice(0, SHOWN).map((f, i) => (
          <Line key={i} tone={findingTone(f)} hollow={!f.firm} text={f.text} title={f.firm ? undefined : "Likely, not yet confirmed"} />)))}
      {panel("Needed from you", missing.length, TONE.blue, "missing", "Nothing missing right now.",
        missing.slice(0, SHOWN).map((m, i) => <Line key={i} tone={TONE.blue} text={missingText(m)} />))}
      {c.plan && (
        <div className="mt-auto border-t border-line pt-3 text-xs leading-relaxed text-faint">
          <b className="mb-0.5 block text-[10px] font-semibold uppercase tracking-[0.08em] text-accent">Next</b>
          <span className="line-clamp-2">{c.plan}</span>
        </div>
      )}
    </>
  );
}

function Line({ tone, text, hollow, title }: { tone: string; text: string; hollow?: boolean; title?: string }) {
  return (
    <li className="flex gap-2.5 text-[13px] leading-snug" title={title}>
      <span className="mt-[0.42em] inline-block h-2 w-2 shrink-0 rounded-full"
        style={hollow ? { boxShadow: `inset 0 0 0 1.5px ${tone}` } : { background: tone }} />
      <span className="line-clamp-2">{text}</span>
    </li>
  );
}

const ICON = { width: 14, height: 14, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2,
  strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
function PinIcon() {
  return <svg {...ICON} width={15} height={15}><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z" /><circle cx="12" cy="9.5" r="2.5" /></svg>;
}

/** Name and place, with a pencil to edit both in place and a bin to delete the project.
 *  Test runs keep their "(test run)" tag. */
function Head({ c, onEdit, onTrash }: { c: ProjectCard; onEdit: (patch: Partial<Project>) => Promise<void>; onTrash: () => Promise<void> }) {
  const [editing, setEditing] = useState(false);
  const [f, setF] = useState({ name: "", region: "", country: "" });
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const first = useRef<HTMLInputElement>(null);
  useEffect(() => { if (editing) first.current?.select(); }, [editing]);
  const stop = (e: React.SyntheticEvent) => e.stopPropagation();
  const place = [c.region, c.country].filter(Boolean).join(", ");
  const open = () => { setF({ name: shortName(c), region: c.region ?? "", country: c.country ?? "" }); setErr(null); setEditing(true); };
  const save = async () => {
    const name = f.name.trim();
    if (!name) { setErr("The name can't be empty."); return; }
    setSaving(true);
    try {
      await onEdit({ name: isTest(c) ? `${name} (test run)` : name, region: f.region.trim(), country: f.country.trim() });
      setEditing(false);
    } catch (e) { setErr(`Not saved: ${e}`); }
    finally { setSaving(false); }
  };
  const tool = "shrink-0 rounded-md p-1 text-faint opacity-60 transition hover:bg-sunken hover:text-fg group-hover:opacity-100";
  const field = "w-full rounded-lg border border-line bg-black/20 px-2.5 py-1.5 text-fg outline-none focus:border-accent";

  if (editing) return (
    <div onClick={stop} className="flex flex-col gap-2"
      onKeyDown={(e) => { stop(e); if (e.key === "Enter") save(); if (e.key === "Escape") setEditing(false); }}>
      <input ref={first} value={f.name} disabled={saving} maxLength={120} aria-label="Project name" data-testid="rename-input"
        onChange={(e) => setF({ ...f, name: e.target.value })}
        className={`${field} text-[17px] font-bold tracking-[-0.025em]`} />
      <div className="flex gap-2">
        <input value={f.region} disabled={saving} placeholder="City" aria-label="City" data-testid="city-input"
          onChange={(e) => setF({ ...f, region: e.target.value })} className={`${field} text-sm`} />
        <input value={f.country} disabled={saving} placeholder="Country" aria-label="Country" data-testid="country-input"
          onChange={(e) => setF({ ...f, country: e.target.value })} className={`${field} text-sm`} />
      </div>
      <div className="flex items-center gap-2">
        <button onClick={save} disabled={saving} data-testid="edit-save"
          className="rounded-full bg-accent px-4 py-1.5 text-xs font-bold text-accent-fg disabled:opacity-60">{saving ? "Saving…" : "Save"}</button>
        <button onClick={() => setEditing(false)} className="rounded-full px-3 py-1.5 text-xs text-faint hover:text-fg">Cancel</button>
        {err && <span className="text-xs text-danger">{err}</span>}
      </div>
    </div>
  );
  return (
    <div>
      <div className="flex items-start gap-1">
        <div className="min-w-0 flex-1 text-[19px] font-bold leading-snug tracking-[-0.025em]">{shortName(c)}</div>
        <button onClick={(e) => { stop(e); open(); }} onKeyDown={stop} aria-label="Edit name and place" title="Edit name and place"
          data-testid="rename" className={tool}>
          <svg {...ICON}><path d="M12 20h9" /><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z" /></svg>
        </button>
        <DeleteProject name={shortName(c)} onDelete={onTrash} className="opacity-60 group-hover:opacity-100" />
      </div>
      <div className="mt-1.5 flex flex-wrap items-center gap-2 text-[14px] text-muted">
        {place ? <span className="flex items-center gap-1.5"><span className="text-accent"><PinIcon /></span>{place}</span>
          : <button onClick={(e) => { stop(e); open(); }} className="flex items-center gap-1.5 text-faint hover:text-fg"><PinIcon />Add city and country</button>}
        {isTest(c) && <span className="rounded-full bg-sunken px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em] text-faint">Test</span>}
      </div>
    </div>
  );
}
