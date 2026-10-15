import { useEffect, useRef, useState } from "react";
import type { ProjectCard } from "../types";
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

/** Card layouts: List (two lists), Panels (two tinted panels), Rail (a lit line through findings, asks and plan),
 *  Focus (the one top finding and the one next ask, large), Tiles (two big counts, then the top of each). */
export const DESIGNS = ["list", "panels", "rail", "focus", "tiles"] as const;
export type Design = (typeof DESIGNS)[number];
const DESIGN_NAME: Record<Design, string> = { list: "List", panels: "Panels", rail: "Rail", focus: "Focus", tiles: "Tiles" };
const DESIGN_KEY = "allfix.cards";
const savedDesign = (): Design => {
  try { const v = localStorage.getItem(DESIGN_KEY); return (DESIGNS as readonly string[]).includes(v ?? "") ? (v as Design) : "list"; }
  catch { return "list"; }
};
const saveDesign = (d: Design) => { try { localStorage.setItem(DESIGN_KEY, d); } catch { /* storage unavailable */ } };

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
  const [design, setDesign] = useState<Design>(savedDesign);
  const pickDesign = (d: Design) => { setDesign(d); saveDesign(d); };
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
          <Picker label="Cards" testid="card-picker" options={DESIGNS} names={DESIGN_NAME} value={design} onPick={pickDesign} />
          <Picker label="Look" testid="look-picker" options={LOOKS} names={LOOK_NAME} value={look} onPick={pick} />
        </div>

        <div className={st.hero === "plain" ? "mb-6" : "mb-10 px-2 max-sm:px-0"}>{header}</div>

        {error ? (
          <div className="flex flex-col items-start gap-2 text-sm text-faint" data-testid="overview-error">
            <span>{error}</span>
            <button onClick={onRetry} className="rounded-full border border-line px-4 py-2 text-fg hover:bg-panel">Try again</button>
          </div>
        ) : !loading && cards.length === 0 ? (
          <div className="text-sm text-faint" data-testid="empty-dashboard">A project holds one business: its research, plan, files and decisions. Start one with New project.</div>
        ) : (
          <div className={`grid grid-cols-[repeat(auto-fill,minmax(290px,1fr))] max-sm:grid-cols-1 ${st.hero === "plain" ? "gap-4" : "gap-5"}`}>
            {sorted.map((c, i) => <Card key={c.id} c={c} n={i + 1} st={st} design={design} onOpen={() => onOpen(c.id)} onRename={(name) => onRename(c.id, name)} />)}
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

function Card({ c, n, st, design, onOpen, onRename }: {
  c: ProjectCard; n: number; st: LookStyle; design: Design; onOpen: () => void; onRename: (name: string) => Promise<void>;
}) {
  const place = [c.region, c.country].filter(Boolean).join(", ");
  const num = String(n).padStart(2, "0");
  return (
    <div role="button" tabIndex={0} onClick={onOpen} onKeyDown={(e) => { if (e.key === "Enter" && e.target === e.currentTarget) onOpen(); }}
      data-testid="project-card"
      className={`frame group relative flex min-w-0 cursor-pointer flex-col gap-4 p-5 text-left text-fg transition duration-300 hover:-translate-y-0.5 ${st.shell}`}>
      {st.hairline && <span aria-hidden className="pointer-events-none absolute inset-x-6 top-0 h-px bg-[linear-gradient(90deg,transparent,rgba(224,148,34,.9),transparent)]" />}
      {st.index === "big" && <span aria-hidden className="pointer-events-none absolute right-5 top-4 text-[34px] font-extralight leading-none tracking-[-0.04em] text-white/[.13] tabular-nums">{num}</span>}
      <div className={st.index === "big" ? "pr-12" : ""}>
        {st.index === "eyebrow" && <div className="mb-2 font-mono text-[11px] tracking-[0.1em] text-accent">{num}</div>}
        <Title c={c} onRename={onRename} />
        <div className="mt-1 flex flex-wrap items-center gap-1.5 text-xs text-faint">
          {place && <span>{place}</span>}
          {isTest(c) && <span className="rounded-full bg-sunken px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em]">Test</span>}
        </div>
      </div>

      {design === "list" ? <ListBody c={c} /> : design === "panels" ? <PanelsBody c={c} />
        : design === "rail" ? <RailBody c={c} /> : design === "focus" ? <FocusBody c={c} /> : <TilesBody c={c} />}
    </div>
  );
}

const emptyFound = (c: ProjectCard) => (c.item_total ? "Nothing important found yet." : "Nothing researched yet.");
const EMPTY_MISSING = "Nothing missing right now.";
const more = (n: number, shown: number) => (n > shown ? <li className="pl-4 text-xs text-faint">+{n - shown} more inside</li> : null);

function PlanLine({ c, label = "Plan" }: { c: ProjectCard; label?: string }) {
  if (!c.plan) return null;
  return (
    <div className="mt-auto border-t border-line pt-3 text-xs leading-relaxed text-faint">
      <b className="mb-0.5 block text-[10px] font-semibold uppercase tracking-[0.08em] text-accent">{label}</b>
      <span className="line-clamp-2">{c.plan}</span>
    </div>
  );
}

/** List: two plain lists, top three of each. */
function ListBody({ c }: { c: ProjectCard }) {
  const findings = c.findings ?? [], missing = c.missing ?? [];
  return (
    <>
      <Section title="Important findings" count={findings.length} testid="findings" empty={emptyFound(c)}>
        {findings.slice(0, SHOWN).map((f, i) => (
          <Line key={i} tone={findingTone(f)} hollow={!f.firm} text={f.text} title={f.firm ? undefined : "Likely, not yet confirmed"} />
        ))}
      </Section>
      <Section title="Missing from you" count={missing.length} testid="missing" empty={EMPTY_MISSING}>
        {missing.slice(0, SHOWN).map((m, i) => <Line key={i} tone={TONE.blue} text={missingText(m)} />)}
      </Section>
      <PlanLine c={c} />
    </>
  );
}

/** Panels: findings in a warm glass panel, asks in a cool one, each with a glowing count. */
function PanelsBody({ c }: { c: ProjectCard }) {
  const findings = c.findings ?? [], missing = c.missing ?? [];
  const panel = (title: string, count: number, tone: string, testid: string, empty: string, rows: React.ReactNode) => (
    <div data-testid={testid} className="rounded-[16px] p-3.5"
      style={{ background: `linear-gradient(180deg, ${tone}1f, ${tone}0a)`, boxShadow: `inset 0 0 0 1px ${tone}33` }}>
      <div className="mb-2.5 flex items-center justify-between">
        <span className="font-mono text-[10.5px] uppercase tracking-[0.18em]" style={{ color: tone }}>{title}</span>
        <span className="grid h-6 min-w-6 place-items-center rounded-full px-1.5 text-[11px] font-bold tabular-nums text-[#111]"
          style={{ background: tone, boxShadow: `0 0 14px ${tone}99`, opacity: count ? 1 : 0.35 }}>{count}</span>
      </div>
      {count === 0 ? <div className="text-[13px] text-faint">{empty}</div>
        : <ul className="flex flex-col gap-2">{rows}{more(count, 2)}</ul>}
    </div>
  );
  return (
    <>
      {panel("Found", findings.length, TONE.amber, "findings", emptyFound(c),
        findings.slice(0, 2).map((f, i) => <Line key={i} tone={findingTone(f)} hollow={!f.firm} text={f.text} />))}
      {panel("Needed from you", missing.length, TONE.blue, "missing", EMPTY_MISSING,
        missing.slice(0, 2).map((m, i) => <Line key={i} tone={TONE.blue} text={missingText(m)} />))}
      <PlanLine c={c} label="Next" />
    </>
  );
}

/** Rail: one lit line runs through what was found, what is needed, then the plan. */
function RailBody({ c }: { c: ProjectCard }) {
  const findings = c.findings ?? [], missing = c.missing ?? [];
  const node = (tone: string, hollow = false) => (
    <span className="absolute -left-[19px] top-[0.35em] h-[9px] w-[9px] rounded-full"
      style={hollow ? { boxShadow: `inset 0 0 0 1.5px ${tone}`, background: "#16171b" } : { background: tone, boxShadow: `0 0 10px ${tone}` }} />
  );
  const group = (label: string, tone: string, count: number, testid: string, rows: React.ReactNode, empty: string) => (
    <div data-testid={testid} className="relative">
      <div className="mb-2 flex items-center gap-2 font-mono text-[10.5px] uppercase tracking-[0.18em]" style={{ color: tone }}>
        {label}<span className="tabular-nums text-faint">{count}</span>
      </div>
      {count === 0 ? <div className="text-[13px] text-faint">{empty}</div> : <ul className="flex flex-col gap-2.5">{rows}{more(count, 2)}</ul>}
    </div>
  );
  const row = (key: number, tone: string, text: string, hollow?: boolean) => (
    <li key={key} className="relative text-[13px] leading-snug">{node(tone, hollow)}<span className="line-clamp-2">{text}</span></li>
  );
  return (
    <div className="relative flex flex-1 flex-col gap-4 pl-[22px]">
      <span aria-hidden className="absolute bottom-1 left-[7px] top-1 w-px"
        style={{ background: `linear-gradient(180deg, ${TONE.amber}, ${TONE.blue} 70%, rgba(224,148,34,.5))`, boxShadow: `0 0 8px ${TONE.amber}66` }} />
      {group("Found", TONE.amber, findings.length, "findings",
        findings.slice(0, 2).map((f, i) => row(i, findingTone(f), f.text, !f.firm)), emptyFound(c))}
      {group("From you", TONE.blue, missing.length, "missing",
        missing.slice(0, 2).map((m, i) => row(i, TONE.blue, missingText(m))), EMPTY_MISSING)}
      {c.plan && (
        <div className="relative mt-auto text-xs leading-relaxed text-faint">
          {node(TONE.amber, true)}
          <b className="mb-0.5 block font-mono text-[10px] font-normal uppercase tracking-[0.18em] text-accent">Plan</b>
          <span className="line-clamp-2">{c.plan}</span>
        </div>
      )}
    </div>
  );
}

/** Focus: the single most important finding and the single next ask, large; the rest as counts. */
function FocusBody({ c }: { c: ProjectCard }) {
  const findings = c.findings ?? [], missing = c.missing ?? [];
  const top = findings[0], ask = missing[0];
  return (
    <>
      <div data-testid="findings">
        <div className="mb-1.5 font-mono text-[10.5px] uppercase tracking-[0.18em] text-faint">Top finding</div>
        {top ? (
          <div className="relative pl-3.5 text-[15px] font-semibold leading-snug tracking-[-0.01em]">
            <span aria-hidden className="absolute bottom-0.5 left-0 top-0.5 w-[3px] rounded-full"
              style={{ background: findingTone(top), boxShadow: `0 0 12px ${findingTone(top)}` }} />
            <span className="line-clamp-3">{top.text}</span>
          </div>
        ) : <div className="text-[13px] text-faint">{emptyFound(c)}</div>}
      </div>
      <div data-testid="missing">
        <div className="mb-1.5 font-mono text-[10.5px] uppercase tracking-[0.18em] text-faint">Answer next</div>
        {ask ? (
          <div className="flex items-start gap-2.5 rounded-[14px] bg-[#4f8fe0]/[.12] px-3.5 py-3 text-[13.5px] leading-snug ring-1 ring-[#4f8fe0]/30">
            <span aria-hidden className="mt-px text-[#7fb0ff]">→</span><span className="line-clamp-2">{missingText(ask)}</span>
          </div>
        ) : <div className="text-[13px] text-faint">{EMPTY_MISSING}</div>}
      </div>
      <div className="flex flex-wrap gap-1.5 text-[11.5px]">
        <Chip tone={TONE.amber} text={`${findings.length} ${findings.length === 1 ? "finding" : "findings"}`} />
        <Chip tone={TONE.blue} text={`${missing.length} from you`} />
      </div>
      <PlanLine c={c} />
    </>
  );
}

function Chip({ tone, text }: { tone: string; text: string }) {
  return (
    <span className="flex items-center gap-1.5 rounded-full bg-white/[.05] px-2.5 py-1 text-faint ring-1 ring-white/[.06]">
      <span className="h-1.5 w-1.5 rounded-full" style={{ background: tone, boxShadow: `0 0 8px ${tone}` }} />{text}
    </span>
  );
}

/** Tiles: two big glowing counts, then the top item of each, tagged. */
function TilesBody({ c }: { c: ProjectCard }) {
  const findings = c.findings ?? [], missing = c.missing ?? [];
  const tile = (n: number, label: string, tone: string) => (
    <div className="flex-1 rounded-[16px] bg-white/[.04] px-3.5 py-3 ring-1 ring-white/[.06]">
      <b className="block text-[32px] font-light leading-none tabular-nums tracking-[-0.03em]"
        style={{ color: n ? tone : undefined, textShadow: n ? `0 0 18px ${tone}88` : undefined }}>{n}</b>
      <span className="mt-1.5 block font-mono text-[10px] uppercase tracking-[0.18em] text-faint">{label}</span>
    </div>
  );
  const tagged = (tag: string, tone: string, text: string, testid: string) => (
    <div data-testid={testid} className="flex items-start gap-2.5 text-[13px] leading-snug">
      <span className="mt-px shrink-0 rounded-md px-1.5 py-0.5 font-mono text-[9.5px] uppercase tracking-[0.14em]"
        style={{ color: tone, boxShadow: `inset 0 0 0 1px ${tone}55` }}>{tag}</span>
      <span className="line-clamp-2">{text}</span>
    </div>
  );
  return (
    <>
      <div className="flex gap-2.5">{tile(findings.length, "Findings", TONE.amber)}{tile(missing.length, "From you", TONE.blue)}</div>
      <div className="flex flex-col gap-3">
        {findings[0] ? tagged("Found", findingTone(findings[0]), findings[0].text, "findings")
          : <div data-testid="findings" className="text-[13px] text-faint">{emptyFound(c)}</div>}
        {missing[0] ? tagged("You", TONE.blue, missingText(missing[0]), "missing")
          : <div data-testid="missing" className="text-[13px] text-faint">{EMPTY_MISSING}</div>}
      </div>
      <PlanLine c={c} />
    </>
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
