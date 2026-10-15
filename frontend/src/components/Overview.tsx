import { useEffect, useRef, useState } from "react";
import type { ProjectCard } from "../types";
import { Orbits } from "./Ignition";

type Finding = ProjectCard["findings"][number];
type Missing = ProjectCard["missing"][number];

/** Page looks: dark cards on a light page (Stone, the default), dark-headed light cards (Duo),
 *  all dark (Night), or a dark summary band over light cards (Band). Picked on the page, kept per browser. */
export const LOOKS = ["stone", "duo", "night", "band"] as const;
export type Look = (typeof LOOKS)[number];
const LOOK_NAME: Record<Look, string> = { stone: "Stone", duo: "Duo", night: "Night", band: "Band" };
const LOOK_KEY = "allfix.look";
const savedLook = (): Look => {
  try { const v = localStorage.getItem(LOOK_KEY); return (LOOKS as readonly string[]).includes(v ?? "") ? (v as Look) : "stone"; }
  catch { return "stone"; }
};
const saveLook = (l: Look) => { try { localStorage.setItem(LOOK_KEY, l); } catch { /* storage unavailable */ } };

const PAGE: Record<Look, { cls: string; bg: string }> = {
  stone: { cls: "sheet", bg: "#e9e7e1" },
  duo: { cls: "sheet", bg: "#efede8" },
  night: { cls: "frame border border-line", bg: "#0d0e11" },
  band: { cls: "sheet", bg: "#f1efea" },
};
/** Card shell and its head; the head is where Duo puts its dark band. */
const CARD: Record<Look, { shell: string; head: string }> = {
  stone: { shell: "frame bg-[#17181c] text-fg shadow-[0_18px_40px_-22px_rgba(0,0,0,.55)] hover:shadow-[0_0_0_2px_var(--accent),0_18px_40px_-22px_rgba(0,0,0,.55)]", head: "" },
  duo: { shell: "bg-white text-fg shadow-[0_1px_0_rgba(0,0,0,.04),0_14px_34px_-24px_rgba(0,0,0,.45)] ring-1 ring-black/5 hover:ring-accent", head: "frame -mx-5 -mt-5 mb-1 min-h-[104px] rounded-t-[22px] bg-[#17181c] px-5 pb-4 pt-5 text-fg" },
  night: { shell: "frame border border-line bg-[linear-gradient(180deg,rgba(32,34,40,.92),rgba(23,24,29,.92))] text-fg hover:border-accent/60", head: "" },
  band: { shell: "bg-white text-fg ring-1 ring-black/5 shadow-[0_14px_34px_-26px_rgba(0,0,0,.4)] hover:ring-accent [box-shadow:inset_0_3px_0_var(--accent)]", head: "" },
};

const TONE = { red: "#e2553a", amber: "#e09422", blue: "#4f8fe0" };
const findingTone = (f: Finding) => (f.kind === "finding" ? TONE.amber : TONE.red);
const missingText = (m: Missing) => (m.kind === "check" ? `Result needed: ${m.text}` : m.text);
const SHOWN = 3;

const isTest = (c: ProjectCard) => /\(test run\)\s*$/i.test(c.name);
const shortName = (c: ProjectCard) => c.name.replace(/\s*\(test run\)\s*$/i, "");
/** Real projects first, then the most recently active. */
const order = (a: ProjectCard, b: ProjectCard) =>
  Number(isTest(a)) - Number(isTest(b)) || String(b.last_activity ?? "").localeCompare(String(a.last_activity ?? ""));

/** All projects at a glance: for each, what was found and what is missing from the owner. */
export default function Overview({ cards, loading, error, onOpen, onNew, onRetry, onRename }: {
  cards: ProjectCard[]; loading: boolean; error: string | null;
  onOpen: (id: string) => void; onNew: () => void; onRetry: () => void;
  onRename: (id: string, name: string) => Promise<void>;
}) {
  const [look, setLook] = useState<Look>(savedLook);
  const pick = (l: Look) => { setLook(l); saveLook(l); };
  const sorted = [...cards].sort(order);
  const findings = cards.reduce((n, c) => n + (c.findings?.length ?? 0), 0);
  const missing = cards.reduce((n, c) => n + (c.missing?.length ?? 0), 0);
  const page = PAGE[look];
  const dark = look === "night";

  const header = (
    <div className="flex flex-wrap items-center gap-x-9 gap-y-4">
      <div className="min-w-0" data-testid="verdict">
        <div className="text-[clamp(22px,3vw,32px)] font-bold leading-[1.15] tracking-[-0.035em]">Your projects</div>
        <div className="mt-1.5 text-sm text-faint">
          {loading ? "Loading…" : error ? "Could not load the projects."
            : cards.length === 0 ? "No projects yet."
            : `${findings} findings to read, ${missing} things only you can give.`}
        </div>
      </div>
      <div className="ml-auto flex flex-wrap items-end gap-7 max-md:ml-0">
        <Kpi n={cards.length} label="Projects" />
        <Kpi n={findings} label="Findings" tone={TONE.amber} />
        <Kpi n={missing} label="From you" tone={TONE.blue} />
        <button onClick={onNew} className="cta !px-5 !py-2.5 !text-sm" data-testid="overview-new">+ New project</button>
      </div>
    </div>
  );

  return (
    <div className={`relative min-w-0 flex-1 overflow-hidden rounded-[22px] ${page.cls}`} style={{ background: page.bg }}
      data-testid="overview" data-look={look}>
      {dark && <Orbits dim />}
      <div className="relative h-full overflow-auto px-6 pb-8 pt-6 scroll-thin max-sm:px-3">
        <div className="mb-4 flex justify-end">
          <div className={`flex items-center gap-1 rounded-full p-1 text-[11.5px] ${dark ? "bg-[#1b1c21]" : "bg-black/[.06]"}`}
            role="radiogroup" aria-label="Page look" data-testid="look-picker">
            <span className="px-2 text-faint">Look</span>
            {LOOKS.map((l) => (
              <button key={l} role="radio" aria-checked={look === l} onClick={() => pick(l)}
                className={`rounded-full px-3 py-1 transition ${look === l ? "bg-accent font-semibold text-accent-fg" : "text-faint hover:text-fg"}`}>
                {LOOK_NAME[l]}
              </button>
            ))}
          </div>
        </div>

        {look === "band"
          ? <div className="frame mb-6 rounded-[20px] bg-[#16171b] px-6 py-5 text-fg">{header}</div>
          : <div className="mb-6">{header}</div>}

        {error ? (
          <div className="flex flex-col items-start gap-2 text-sm text-faint" data-testid="overview-error">
            <span>{error}</span>
            <button onClick={onRetry} className="rounded-full border border-line px-4 py-2 text-fg hover:bg-panel">Try again</button>
          </div>
        ) : !loading && cards.length === 0 ? (
          <div className="text-sm text-faint" data-testid="empty-dashboard">A project holds one business: its research, plan, files and decisions. Start one with New project.</div>
        ) : (
          <div className="grid grid-cols-[repeat(auto-fill,minmax(290px,1fr))] gap-4 max-sm:grid-cols-1">
            {sorted.map((c) => <Card key={c.id} c={c} look={look} onOpen={() => onOpen(c.id)} onRename={(n) => onRename(c.id, n)} />)}
          </div>
        )}
      </div>
    </div>
  );
}

function Kpi({ n, label, tone }: { n: number; label: string; tone?: string }) {
  return (
    <div className="flex flex-col gap-1">
      <b className="text-[30px] font-light tabular-nums tracking-[-0.03em]">{n}</b>
      <span className="flex items-center gap-1.5 text-[11px] uppercase tracking-[0.08em] text-faint">
        {tone && <span className="h-2 w-2 rounded-full" style={{ background: tone }} />}{label}
      </span>
    </div>
  );
}

function Card({ c, look, onOpen, onRename }: { c: ProjectCard; look: Look; onOpen: () => void; onRename: (name: string) => Promise<void> }) {
  const place = [c.region, c.country].filter(Boolean).join(", ");
  const findings = c.findings ?? [];
  const missing = c.missing ?? [];
  const style = CARD[look];
  return (
    <div role="button" tabIndex={0} onClick={onOpen} onKeyDown={(e) => { if (e.key === "Enter" && e.target === e.currentTarget) onOpen(); }}
      data-testid="project-card"
      className={`group flex min-w-0 cursor-pointer flex-col gap-4 rounded-[22px] p-5 text-left transition hover:-translate-y-0.5 ${style.shell}`}>
      <div className={style.head}>
        <Title c={c} onRename={onRename} />
        <div className="mt-1 flex flex-wrap items-center gap-1.5 text-xs text-faint">
          {place && <span>{place}</span>}
          {isTest(c) && <span className="rounded-full bg-sunken px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em]">Test</span>}
        </div>
      </div>

      <Section title="Important findings" count={findings.length} testid="findings"
        empty={c.item_total ? "Nothing important found yet." : "Nothing researched yet."}>
        {findings.slice(0, SHOWN).map((f, i) => (
          <Line key={i} tone={findingTone(f)} hollow={!f.firm} text={f.text} title={f.firm ? undefined : "Likely, not yet confirmed"} />
        ))}
      </Section>

      <Section title="Missing from you" count={missing.length} testid="missing" empty="Nothing missing right now.">
        {missing.slice(0, SHOWN).map((m, i) => <Line key={i} tone={TONE.blue} text={missingText(m)} />)}
      </Section>

      {c.plan && (
        <div className="mt-auto border-t border-line pt-3 text-xs leading-relaxed text-faint">
          <b className="mb-0.5 block text-[10px] font-semibold uppercase tracking-[0.08em] text-accent">Plan</b>
          <span className="line-clamp-2">{c.plan}</span>
        </div>
      )}
    </div>
  );
}

function Section({ title, count, empty, testid, children }: {
  title: string; count: number; empty: string; testid: string; children: React.ReactNode;
}) {
  return (
    <div data-testid={testid}>
      <div className="mb-2 flex items-baseline justify-between text-[10.5px] font-semibold uppercase tracking-[0.08em] text-faint">
        <span>{title}</span>{count > 0 && <span className="tabular-nums">{count}</span>}
      </div>
      {count === 0 ? <div className="text-[13px] text-faint">{empty}</div> : (
        <ul className="flex flex-col gap-2">
          {children}
          {count > SHOWN && <li className="pl-4 text-xs text-faint">+{count - SHOWN} more inside</li>}
        </ul>
      )}
    </div>
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

/** The project name, with a pencil to rename it in place. Test runs keep their "(test run)" tag. */
function Title({ c, onRename }: { c: ProjectCard; onRename: (name: string) => Promise<void> }) {
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState(shortName(c));
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => { if (editing) input.current?.select(); }, [editing]);
  const stop = (e: React.SyntheticEvent) => e.stopPropagation();
  const cancel = () => { setEditing(false); setValue(shortName(c)); setErr(null); };
  const save = async () => {
    const name = value.trim();
    if (!name || name === shortName(c)) { cancel(); return; }
    setSaving(true);
    try { await onRename(isTest(c) ? `${name} (test run)` : name); setEditing(false); setErr(null); }
    catch (e) { setErr(`Not saved: ${e}`); }
    finally { setSaving(false); }
  };

  if (editing) return (
    <div onClick={stop} onKeyDown={stop}>
      <input ref={input} value={value} disabled={saving} maxLength={120} aria-label="Project name" data-testid="rename-input"
        onChange={(e) => setValue(e.target.value)} onBlur={save}
        onKeyDown={(e) => { if (e.key === "Enter") save(); if (e.key === "Escape") cancel(); }}
        className="w-full rounded-lg border border-accent bg-transparent px-2 py-1 text-[17px] font-bold tracking-[-0.025em] text-fg outline-none" />
      {err && <div className="mt-1 text-xs text-danger">{err}</div>}
    </div>
  );
  return (
    <div className="flex items-start gap-2">
      <div className="min-w-0 text-[17px] font-bold leading-snug tracking-[-0.025em]">{shortName(c)}</div>
      <button onClick={(e) => { stop(e); setValue(shortName(c)); setEditing(true); }} onKeyDown={stop}
        aria-label="Rename project" title="Rename" data-testid="rename"
        className="mt-0.5 shrink-0 rounded-md p-1 text-faint opacity-60 transition hover:bg-sunken hover:text-fg group-hover:opacity-100">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 20h9" /><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z" />
        </svg>
      </button>
    </div>
  );
}
