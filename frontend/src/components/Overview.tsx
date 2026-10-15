import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { Project, ProjectCard, TrashedProject } from "../types";
import { Orbits } from "./Ignition";

type Finding = ProjectCard["findings"][number];
type Missing = ProjectCard["missing"][number];

/** Page looks, all "Stone": dark cards on a light page. Stone is the plain one; Halo is the default; Ember, Atelier and Halo
 *  carry the entrance page's finish (mono eyebrow, big type with the amber dot, orbits, glow).
 *  Picked on the page, kept per browser. */
export const LOOKS = ["stone", "ember", "atelier", "halo"] as const;
export type Look = (typeof LOOKS)[number];
const LOOK_NAME: Record<Look, string> = { stone: "Stone", ember: "Ember", atelier: "Atelier", halo: "Halo" };
const LOOK_KEY = "allfix.look";
const savedLook = (): Look => {
  try { const v = localStorage.getItem(LOOK_KEY); return (LOOKS as readonly string[]).includes(v ?? "") ? (v as Look) : "halo"; }
  catch { return "halo"; }
};
const saveLook = (l: Look) => { try { localStorage.setItem(LOOK_KEY, l); } catch { /* storage unavailable */ } };

const GRAIN = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .05 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")";

type LookStyle = {
  bg: string; orbits: boolean; hero: "plain" | "left" | "editorial" | "center";
  shell: string; index: "none" | "eyebrow" | "big"; hairline: boolean;
};
const LOOK: Record<Look, LookStyle> = {
  stone: {
    bg: "#e9e7e1", orbits: false, hero: "plain", index: "none", hairline: false,
    shell: "rounded-[22px] bg-[#17181c] shadow-[0_18px_40px_-22px_rgba(0,0,0,.55)] hover:shadow-[0_0_0_2px_var(--accent),0_18px_40px_-22px_rgba(0,0,0,.55)]",
  },
  ember: {
    bg: "radial-gradient(900px 520px at 88% -8%, rgba(224,148,34,.20), transparent 62%), radial-gradient(700px 420px at 0% 110%, rgba(224,148,34,.08), transparent 60%), #ebe8e1",
    orbits: true, hero: "left", index: "eyebrow", hairline: true,
    shell: "rounded-[24px] bg-[linear-gradient(180deg,#1d1e23,#121317)] ring-1 ring-white/[.06] shadow-[0_30px_60px_-32px_rgba(40,24,0,.75)] hover:shadow-[0_0_0_6px_rgba(224,148,34,.14),0_0_44px_rgba(224,148,34,.38),0_30px_60px_-32px_rgba(40,24,0,.75)]",
  },
  atelier: {
    bg: `${GRAIN}, linear-gradient(180deg,#f1ece3,#e7e1d6)`, orbits: false, hero: "editorial", index: "big", hairline: false,
    shell: "rounded-[14px] bg-[#18191d] shadow-[0_1px_0_rgba(255,255,255,.04)_inset,0_24px_48px_-30px_rgba(30,20,5,.7)] hover:shadow-[0_0_0_1.5px_var(--accent),0_24px_48px_-30px_rgba(30,20,5,.7)]",
  },
  halo: {
    bg: "radial-gradient(1100px 520px at 50% -12%, rgba(224,148,34,.22), transparent 64%), #efede8",
    orbits: true, hero: "center", index: "eyebrow", hairline: false,
    shell: "rounded-[26px] bg-[radial-gradient(420px_220px_at_100%_0%,rgba(224,148,34,.16),transparent_62%),linear-gradient(180deg,rgba(28,29,34,.96),rgba(17,18,22,.96))] ring-1 ring-white/[.08] backdrop-blur shadow-[0_34px_70px_-36px_rgba(30,18,0,.8)] hover:ring-accent/70 hover:shadow-[0_0_0_6px_rgba(224,148,34,.12),0_0_50px_rgba(224,148,34,.3),0_34px_70px_-36px_rgba(30,18,0,.8)]",
  },
};
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
  const [trash, setTrash] = useState<TrashedProject[]>([]);
  const [binOpen, setBinOpen] = useState(false);
  const [undo, setUndo] = useState<{ id: string; name: string } | null>(null);
  const [binErr, setBinErr] = useState<string | null>(null);
  const loadTrash = () => api.trash().then(setTrash).catch(() => setTrash([]));
  useEffect(() => { loadTrash(); }, []);
  useEffect(() => { if (!undo) return; const t = setTimeout(() => setUndo(null), 8000); return () => clearTimeout(t); }, [undo]);
  const act = async (fn: () => Promise<void>) => {
    setBinErr(null);
    try { await fn(); } catch (e) { setBinErr(String(e)); }
    loadTrash(); onChanged();
  };
  const trashProject = (c: ProjectCard) => act(async () => { await api.trashProject(c.id); setUndo({ id: c.id, name: shortName(c) }); });
  const restore = (id: string) => act(async () => { await api.restoreProject(id); setUndo(null); });
  const deleteForever = (id: string) => act(() => api.deleteProject(id));
  const toggleBin = () => { if (!binOpen) loadTrash(); setBinOpen(!binOpen); };
  const [look, setLook] = useState<Look>(savedLook);
  const pick = (l: Look) => { setLook(l); saveLook(l); };
  const sorted = [...cards].sort(order);
  const findings = cards.reduce((n, c) => n + (c.findings?.length ?? 0), 0);
  const missing = cards.reduce((n, c) => n + (c.missing?.length ?? 0), 0);
  const st = LOOK[look];
  const summary = loading ? "Loading…" : error ? "Could not load the projects."
    : cards.length === 0 ? "No projects yet." : `${findings} findings to read, ${missing} things only you can give.`;
  const kpis = (
    <>
      <Kpi n={cards.length} label="Projects" premium={st.hero !== "plain"} />
      <Kpi n={findings} label="Findings" tone={TONE.amber} premium={st.hero !== "plain"} />
      <Kpi n={missing} label="From you" tone={TONE.blue} premium={st.hero !== "plain"} />
    </>
  );
  const eyebrow = <div className="font-mono text-[11px] uppercase tracking-[0.32em] text-faint">AllFix · Projects · {today()}</div>;
  const newBtn = <button onClick={onNew} className="cta !px-5 !py-2.5 !text-sm" data-testid="overview-new">+ New project</button>;

  const header = st.hero === "plain" ? (
    <div className="flex flex-wrap items-center gap-x-9 gap-y-4">
      <div className="min-w-0" data-testid="verdict">
        <div className="text-[clamp(22px,3vw,32px)] font-bold leading-[1.15] tracking-[-0.035em]">Your projects</div>
        <div className="mt-1.5 text-sm text-faint">{summary}</div>
      </div>
      <div className="ml-auto flex flex-wrap items-end gap-7 max-md:ml-0">{kpis}{newBtn}</div>
    </div>
  ) : st.hero === "center" ? (
    <div className="flex flex-col items-center gap-4 pb-2 pt-4 text-center" data-testid="verdict">
      {eyebrow}
      <h1 className="text-[clamp(40px,6vw,76px)] font-extrabold leading-[0.95] tracking-[-0.045em]">Your projects<span className="text-accent">.</span></h1>
      <div className="text-[15px] text-faint">{summary}</div>
      <div className="mt-2 flex flex-wrap items-end justify-center gap-10">{kpis}</div>
      <div className="mt-3">{newBtn}</div>
    </div>
  ) : (
    <div className="flex flex-wrap items-end gap-x-10 gap-y-6" data-testid="verdict">
      <div className="min-w-0 flex flex-col gap-3">
        {eyebrow}
        <h1 className={st.hero === "editorial"
          ? "text-[clamp(40px,5.6vw,72px)] font-light leading-[0.95] tracking-[-0.05em]"
          : "text-[clamp(40px,5.4vw,68px)] font-extrabold leading-[0.95] tracking-[-0.045em]"}>
          {st.hero === "editorial" ? <>Your <b className="font-extrabold">projects</b></> : "Your projects"}<span className="text-accent">.</span>
        </h1>
        <div className="text-[15px] text-faint">{summary}</div>
      </div>
      <div className={`ml-auto flex flex-wrap items-end max-md:ml-0 ${st.hero === "editorial" ? "divide-x divide-black/10 [&>*]:px-8 [&>*:first-child]:pl-0 [&>*:last-child]:pr-0" : "gap-8"}`}>
        {kpis}
      </div>
      <div className="max-md:w-full">{newBtn}</div>
    </div>
  );

  return (
    <div className="sheet relative min-w-0 flex-1 overflow-hidden rounded-[22px]" style={{ background: st.bg }}
      data-testid="overview" data-look={look}>
      {st.orbits && <div className="pointer-events-none absolute inset-x-0 top-0 h-[520px] opacity-90"><Orbits /></div>}
      <div className="relative h-full overflow-auto px-6 pb-10 pt-6 scroll-thin max-sm:px-3">
        <div className="mb-4 flex flex-wrap justify-end gap-2">
          <button onClick={toggleBin} data-testid="bin-open"
            className={`flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-[11.5px] backdrop-blur transition ${binOpen ? "bg-accent font-semibold text-accent-fg" : "bg-black/[.06] text-faint hover:text-fg"}`}>
            <TrashIcon />Recycle bin{trash.length ? ` (${trash.length})` : ""}
          </button>
          <Picker label="Look" testid="look-picker" options={LOOKS} names={LOOK_NAME} value={look} onPick={pick} />
        </div>

        <div className={st.hero === "plain" ? "mb-6" : "mb-10 px-2 max-sm:px-0"}>{header}</div>

        {binOpen && <Bin items={trash} onRestore={restore} onDelete={deleteForever} />}
        {binErr && <div className="mb-4 text-sm text-danger">{binErr}</div>}
        {undo && (
          <div className="frame fixed bottom-6 left-1/2 z-30 flex -translate-x-1/2 items-center gap-4 rounded-full bg-[#17181c] py-2.5 pl-5 pr-2.5 text-sm text-fg shadow-[0_20px_50px_-20px_rgba(0,0,0,.8)] ring-1 ring-white/10"
            data-testid="undo-toast">
            <span>{undo.name} moved to the recycle bin</span>
            <button onClick={() => restore(undo.id)} className="rounded-full bg-accent px-4 py-1.5 text-xs font-bold text-accent-fg">Undo</button>
          </div>
        )}
        {error ? (
          <div className="flex flex-col items-start gap-2 text-sm text-faint" data-testid="overview-error">
            <span>{error}</span>
            <button onClick={onRetry} className="rounded-full border border-line px-4 py-2 text-fg hover:bg-panel">Try again</button>
          </div>
        ) : !loading && cards.length === 0 ? (
          <div className="text-sm text-faint" data-testid="empty-dashboard">A project holds one business: its research, plan, files and decisions. Start one with New project.</div>
        ) : (
          <div className={`grid grid-cols-[repeat(auto-fill,minmax(290px,1fr))] max-sm:grid-cols-1 ${st.hero === "plain" ? "gap-4" : "gap-5"}`}>
            {sorted.map((c, i) => <Card key={c.id} c={c} n={i + 1} st={st} onOpen={() => onOpen(c.id)}
              onEdit={(patch) => onEdit(c.id, patch)} onTrash={() => trashProject(c)} />)}
          </div>
        )}
      </div>
    </div>
  );
}

function Picker<T extends string>({ label, testid, options, names, value, onPick }: {
  label: string; testid: string; options: readonly T[]; names: Record<T, string>; value: T; onPick: (v: T) => void;
}) {
  return (
    <div className="flex items-center gap-1 rounded-full bg-black/[.06] p-1 text-[11.5px] backdrop-blur"
      role="radiogroup" aria-label={label} data-testid={testid}>
      <span className="px-2 text-faint">{label}</span>
      {options.map((o) => (
        <button key={o} role="radio" aria-checked={value === o} onClick={() => onPick(o)}
          className={`rounded-full px-3 py-1 transition ${value === o ? "bg-accent font-semibold text-accent-fg" : "text-faint hover:text-fg"}`}>
          {names[o]}
        </button>
      ))}
    </div>
  );
}

function Kpi({ n, label, tone, premium }: { n: number; label: string; tone?: string; premium?: boolean }) {
  return (
    <div className="flex flex-col gap-1">
      <b className={`font-light tabular-nums tracking-[-0.03em] ${premium ? "text-[44px] leading-none" : "text-[30px]"}`}>{n}</b>
      <span className={`flex items-center gap-1.5 uppercase text-faint ${premium ? "font-mono text-[10.5px] tracking-[0.22em]" : "text-[11px] tracking-[0.08em]"}`}>
        {tone && <span className="h-2 w-2 rounded-full" style={{ background: tone }} />}{label}
      </span>
    </div>
  );
}

function Card({ c, n, st, onOpen, onEdit, onTrash }: {
  c: ProjectCard; n: number; st: LookStyle; onOpen: () => void;
  onEdit: (patch: Partial<Project>) => Promise<void>; onTrash: () => void;
}) {
  const num = String(n).padStart(2, "0");
  return (
    <div role="button" tabIndex={0} onClick={onOpen} onKeyDown={(e) => { if (e.key === "Enter" && e.target === e.currentTarget) onOpen(); }}
      data-testid="project-card"
      className={`frame group relative flex min-w-0 cursor-pointer flex-col gap-4 p-5 text-left text-fg transition duration-300 hover:-translate-y-0.5 ${st.shell}`}>
      {st.hairline && <span aria-hidden className="pointer-events-none absolute inset-x-6 top-0 h-px bg-[linear-gradient(90deg,transparent,rgba(224,148,34,.9),transparent)]" />}
      {st.index === "big" && <span aria-hidden className="pointer-events-none absolute right-5 top-4 text-[34px] font-extralight leading-none tracking-[-0.04em] text-white/[.13] tabular-nums">{num}</span>}
      <div className={st.index === "big" ? "pr-12" : ""}>
        {st.index === "eyebrow" && <div className="mb-2 font-mono text-[11px] tracking-[0.1em] text-accent">{num}</div>}
        <Head c={c} onEdit={onEdit} onTrash={onTrash} />
      </div>
      <Panels c={c} />
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
function TrashIcon() {
  return <svg {...ICON}><path d="M3 6h18" /><path d="M8 6V4h8v2" /><path d="M19 6l-1 14H6L5 6" /><path d="M10 11v6M14 11v6" /></svg>;
}
function PinIcon() {
  return <svg {...ICON} width={15} height={15}><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z" /><circle cx="12" cy="9.5" r="2.5" /></svg>;
}

/** Name and place, with a pencil to edit both in place and a bin to move the project to the recycle bin.
 *  Test runs keep their "(test run)" tag. */
function Head({ c, onEdit, onTrash }: { c: ProjectCard; onEdit: (patch: Partial<Project>) => Promise<void>; onTrash: () => void }) {
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
        <button onClick={(e) => { stop(e); onTrash(); }} onKeyDown={stop} aria-label="Move to recycle bin" title="Move to recycle bin"
          data-testid="trash" className={`${tool} hover:!text-[#f07a5f]`}><TrashIcon /></button>
      </div>
      <div className="mt-1.5 flex flex-wrap items-center gap-2 text-[14px] text-muted">
        {place ? <span className="flex items-center gap-1.5"><span className="text-accent"><PinIcon /></span>{place}</span>
          : <button onClick={(e) => { stop(e); open(); }} className="flex items-center gap-1.5 text-faint hover:text-fg"><PinIcon />Add city and country</button>}
        {isTest(c) && <span className="rounded-full bg-sunken px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em] text-faint">Test</span>}
      </div>
    </div>
  );
}

/** Deleted projects wait here: restore one, or delete it forever (asked twice). */
function Bin({ items, onRestore, onDelete }: {
  items: TrashedProject[]; onRestore: (id: string) => void; onDelete: (id: string) => void;
}) {
  const [sure, setSure] = useState<string | null>(null);
  return (
    <div className="frame mb-8 rounded-[22px] bg-[linear-gradient(180deg,rgba(28,29,34,.97),rgba(17,18,22,.97))] p-5 text-fg ring-1 ring-white/[.08]"
      data-testid="bin">
      <div className="mb-1 font-mono text-[10.5px] uppercase tracking-[0.18em] text-accent">Recycle bin</div>
      <div className="mb-4 text-[13px] text-faint">Deleted projects keep everything here until you delete them forever.</div>
      {items.length === 0 ? <div className="text-sm text-faint">The bin is empty.</div> : (
        <ul className="flex flex-col divide-y divide-white/[.06]">
          {items.map((t) => (
            <li key={t.id} className="flex flex-wrap items-center gap-3 py-3" data-testid="bin-item">
              <div className="min-w-0 flex-1">
                <div className="text-[15px] font-semibold">{t.name.replace(/\s*\(test run\)\s*$/i, "")}</div>
                <div className="text-xs text-faint">
                  {[t.region, t.country].filter(Boolean).join(", ") || "No place set"} · deleted {new Date(t.deleted_at).toLocaleDateString("en-GB", { day: "numeric", month: "short" })}
                </div>
              </div>
              <button onClick={() => onRestore(t.id)} data-testid="bin-restore"
                className="rounded-full bg-accent px-4 py-1.5 text-xs font-bold text-accent-fg">Restore</button>
              {sure === t.id ? (
                <button onClick={() => { setSure(null); onDelete(t.id); }} data-testid="bin-delete-sure"
                  className="rounded-full bg-[#e2553a] px-4 py-1.5 text-xs font-bold text-white">Yes, delete forever</button>
              ) : (
                <button onClick={() => setSure(t.id)} data-testid="bin-delete"
                  className="rounded-full px-3 py-1.5 text-xs text-faint ring-1 ring-white/10 hover:text-[#f07a5f]">Delete forever</button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
