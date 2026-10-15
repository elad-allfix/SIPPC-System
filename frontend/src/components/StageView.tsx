import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { Item, Label, StageView as View, StageViewState, Tone, ViewBlock, ViewFlag, ViewKpi } from "../types";
import Icon from "./Icon";
import { LABEL_NAME, LabelDot } from "./ui";

/** Loads the stage's summary; when the stage changed since it was written, asks for a new one and
 * keeps showing the old one until it arrives. */
export function useStageView(projectId: string, stage: number, version: string, enabled: boolean) {
  const [state, setState] = useState<StageViewState | null>(null);
  const asked = useRef<string>("");
  useEffect(() => {
    if (!enabled) { setState(null); return; }
    let alive = true;
    let timer: number | undefined;
    const key = `${projectId}:${stage}:${version}`;
    setState((s) => (asked.current.startsWith(`${projectId}:${stage}:`) ? s : null));
    const poll = async () => {
      try {
        let s = await api.stageView(projectId, stage);
        if (!s.fresh && !s.generating && !s.error && asked.current !== key) {
          asked.current = key;
          s = await api.refreshStageView(projectId, stage);
        }
        if (!alive) return;
        setState(s);
        if (s.generating) timer = window.setTimeout(poll, 2500);
      } catch (e) {
        if (alive) setState((old) => ({ view: old?.view ?? null, fresh: false, empty: false, generating: false, error: String(e) }));
      }
    };
    poll();
    return () => { alive = false; window.clearTimeout(timer); };
  }, [projectId, stage, version, enabled]);
  const retry = async () => {
    try { setState(await api.refreshStageView(projectId, stage)); } catch { /* shown on next poll */ }
    asked.current = "";
  };
  return { state, retry };
}

const toneText: Record<Tone, string> = { good: "text-[#1f8a5f]", bad: "text-danger", neutral: "text-fg" };
const toneDark: Record<Tone, string> = { good: "text-[#7fd6ad]", bad: "text-[#ff9b73]", neutral: "text-frame-fg" };
const toneFill: Record<Tone, string> = { good: "#1f8a5f", bad: "#c2410c", neutral: "#8a8c95" };

/** "**Merge** the campaigns" -> bold where the model asked for it, nothing else. */
function Rich({ text }: { text: string }) {
  return <>{text.split(/(\*\*[^*]+\*\*)/).map((part, i) =>
    part.startsWith("**") ? <b key={i} className="font-semibold text-fg">{part.slice(2, -2)}</b> : part)}</>;
}

function Flags({ flags }: { flags: ViewFlag[] }) {
  if (!flags?.length) return null;
  return (
    <div className="flex flex-wrap gap-1.5">
      {flags.map((f, i) => (
        <span key={i} className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${
          f.tone === "bad" ? "bg-[#fdecea] text-danger" : f.tone === "good" ? "bg-[#e7f4ee] text-[#1f8a5f]" : "bg-sunken text-muted"}`}>
          {f.tone === "bad" ? "✕ " : f.tone === "good" ? "✓ " : ""}{f.text}
        </span>
      ))}
    </div>
  );
}

function Kpi({ k }: { k: ViewKpi }) {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-frame px-3.5 pb-3 pt-3.5 text-frame-fg" data-testid="view-kpi">
      <span className="absolute inset-x-0 top-0 h-0.5 bg-accent" />
      <div className="mb-2.5 flex items-center justify-between">
        <span className="grid h-7 w-7 place-items-center rounded-lg bg-accent/15 text-[#f3b14b]"><Icon name={k.icon} className="h-4 w-4" /></span>
        <LabelDot label={k.evidence as Label} className="!h-2 !w-2 opacity-80" />
      </div>
      <div className={`break-words font-bold leading-tight tracking-tight ${k.value.length > 9 ? "text-[17px]" : "text-[22px]"} ${toneDark[k.tone]}`}>
        {k.value}{k.unit && <span className="ml-1 text-xs font-medium text-frame-muted">{k.unit}</span>}
      </div>
      <div className="mt-0.5 text-xs leading-snug text-frame-muted">{k.label}</div>
    </div>
  );
}

const BLOCK_TINT: Record<string, string> = {
  ad: "bg-[#e8f0fe] text-[#1a73e8]", page: "bg-accent-soft text-accent-ink", searches: "bg-[#eef6ee] text-[#1f8a5f]",
  places: "bg-[#eef3fb] text-[#2d6fb8]", competitors: "bg-[#f4effb] text-[#7a5cc4]",
};

function Block({ b, onAskItem }: { b: ViewBlock; onAskItem: (id: string) => void }) {
  return (
    <section className="flex flex-col gap-3 rounded-[18px] border border-line bg-panel p-4" data-testid="view-block" data-type={b.type}>
      <header className="flex items-center gap-2.5 text-[13px] font-semibold">
        <span className={`grid h-7 w-7 shrink-0 place-items-center rounded-lg ${BLOCK_TINT[b.type] ?? "bg-sunken text-muted"}`}>
          <Icon name={b.icon} className="h-[15px] w-[15px]" stroke={2.2} />
        </span>
        <span className="truncate">{b.title}</span>
      </header>
      <BlockBody b={b} onAskItem={onAskItem} />
      {b.note && <p className="text-[12.5px] leading-relaxed text-muted"><Rich text={b.note} /></p>}
    </section>
  );
}

function BlockBody({ b, onAskItem }: { b: ViewBlock; onAskItem: (id: string) => void }) {
  switch (b.type) {
    case "ad": {
      const hl = b.highlight && b.headline.includes(b.highlight) ? b.headline.split(b.highlight) : null;
      return (<>
        <div className="rounded-xl border border-line bg-white px-3.5 py-3 font-[Arial,Helvetica,sans-serif]">
          <div className="text-[11px] font-bold text-[#202124]">Sponsored</div>
          {b.url && <div className="mb-0.5 truncate text-xs text-[#4d5156]">{b.url}</div>}
          <div className="text-[17px] leading-snug text-[#1a0dab]">
            {hl ? <>{hl[0]}<mark className="rounded bg-[#fde1d6] px-0.5 text-danger">{b.highlight}</mark>{hl.slice(1).join(b.highlight)}</> : b.headline}
          </div>
          {b.description && <div className="mt-1 text-[13px] leading-snug text-[#4d5156]">{b.description}</div>}
        </div>
        <Flags flags={b.flags} />
      </>);
    }
    case "page": {
      const v = b.score?.value ?? 0;
      return (<>
        <div className="flex overflow-hidden rounded-xl border border-line bg-white">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5 border-b border-line bg-sunken px-2.5 py-1.5">
              {[0, 1, 2].map((i) => <i key={i} className="h-2 w-2 rounded-full bg-[#d6d6d2]" />)}
              <span className="ml-1.5 min-w-0 flex-1 truncate rounded-full bg-white px-2.5 py-0.5 text-[11px] text-muted">🔒 {b.url}</span>
            </div>
            <div className="flex flex-col gap-1.5 px-3 py-2.5">
              <div className="truncate text-xs font-bold">{b.heading}</div>
              {[92, 84, 88, 58].map((w) => <i key={w} className="h-1.5 rounded bg-[#ececea]" style={{ width: `${w}%` }} />)}
              {b.cta_after_words ? (
                <div className="mt-0.5 flex items-center gap-2 text-[11px] font-semibold text-danger">
                  <span className="rounded-md bg-danger px-2 py-1 text-[10px] font-bold text-white">Call now</span>after {b.cta_after_words} words
                </div>) : null}
            </div>
          </div>
          {b.score && (
            <div className="flex w-28 shrink-0 flex-col items-center justify-center gap-1 border-l border-line p-2 text-center">
              <svg width="58" height="58" viewBox="0 0 36 36" aria-hidden="true">
                <circle cx="18" cy="18" r="15" fill="none" stroke="#ececea" strokeWidth="4" />
                <circle cx="18" cy="18" r="15" fill="none" stroke={v >= 80 ? "#1f8a5f" : v >= 60 ? "#c2410c" : "#b91c1c"} strokeWidth="4"
                  strokeLinecap="round" strokeDasharray={`${(v / 100) * 94.2} 94.2`} transform="rotate(-90 18 18)" />
                <text x="18" y="21.5" textAnchor="middle" fontSize="9" fontWeight="700" fill="#16171a">{Math.round(v)}%</text>
              </svg>
              <div className="text-[10.5px] leading-tight text-faint">{b.score.label}{b.score.compare && <><br />{b.score.compare}</>}</div>
            </div>
          )}
        </div>
        <Flags flags={b.flags} />
      </>);
    }
    case "searches":
      return (<>
        {b.share.length > 0 && (<div>
          <div className="flex h-2.5 overflow-hidden rounded-full bg-sunken">
            {b.share.map((s, i) => <i key={i} style={{ width: `${s.pct}%`, background: toneFill[s.tone] }} title={`${s.label} ${s.pct}%`} />)}
          </div>
          <div className="mt-1.5 flex flex-wrap justify-between gap-x-3 text-[11px] text-faint">
            {b.share.map((s, i) => <span key={i} className={s.tone === "bad" ? "text-danger" : ""}>{s.label} {s.pct}%</span>)}
          </div>
        </div>)}
        {b.rows.map((r, i) => {
          const parts = r.bold && r.query.includes(r.bold) ? r.query.split(r.bold) : null;
          return (
            <div key={i} className="flex items-center gap-2 rounded-full border border-line bg-white px-3 py-1.5 text-[13px]">
              <Icon name="search" className="h-3.5 w-3.5 shrink-0 text-faint" />
              <span className="min-w-0 flex-1 truncate">{parts ? <>{parts[0]}<b>{r.bold}</b>{parts.slice(1).join(r.bold)}</> : r.query}</span>
              {r.value && <span className="shrink-0 text-xs font-bold text-danger">{r.value}</span>}
            </div>);
        })}
      </>);
    case "timeline":
      return (
        <div className="relative flex items-start pt-1">
          <span className="absolute inset-x-4 top-[19px] h-0.5 bg-line" />
          {b.steps.map((s, i) => (
            <div key={i} className="relative flex min-w-0 flex-1 flex-col items-center gap-1 px-1 text-center">
              <b className={`grid h-[30px] w-[30px] place-items-center rounded-full border-2 bg-panel text-[12px] ${
                s.tone === "bad" ? "border-danger text-danger" : s.tone === "good" ? "border-[#1f8a5f] text-[#1f8a5f]" : "border-line"}`}>{s.symbol || "•"}</b>
              <span className="text-[11px] text-faint">{s.date}</span>
              <span className="text-[12px] font-semibold leading-tight">{s.label}</span>
            </div>
          ))}
        </div>);
    case "bars": {
      const max = Math.max(...b.rows.map((r) => Math.abs(r.value)), 1);
      return (
        <div className="space-y-2">
          {b.rows.map((r, i) => (
            <div key={i}>
              <div className="mb-1 flex justify-between gap-2 text-[12.5px]"><span className="truncate">{r.label}</span>
                <span className={`shrink-0 font-semibold tabular-nums ${toneText[r.tone]}`}>{r.display || r.value}</span></div>
              <div className="h-2 overflow-hidden rounded-full bg-sunken">
                <i className="block h-full rounded-full" style={{ width: `${(Math.abs(r.value) / max) * 100}%`, background: r.tone === "neutral" ? "var(--accent)" : toneFill[r.tone] }} />
              </div>
            </div>
          ))}
        </div>);
    }
    case "profile":
      return (
        <div className="divide-y divide-line">
          {b.rows.map((r, i) => (
            <div key={i} className="flex items-start gap-3 py-2 first:pt-0 last:pb-0">
              <span className="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-sunken text-muted"><Icon name={r.icon} className="h-3.5 w-3.5" /></span>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-1.5 text-[11px] text-faint">{r.label}<LabelDot label={r.evidence} className="!h-1.5 !w-1.5" /></div>
                <div className="text-[13.5px] font-medium leading-snug">{r.value}</div>
              </div>
            </div>
          ))}
        </div>);
    case "list":
      return (
        <ul className="space-y-1.5">
          {b.rows.map((r, i) => (
            <li key={i} className="group flex items-start gap-2.5 rounded-xl bg-sunken px-3 py-2 text-[13px] leading-snug">
              <span className={`mt-0.5 shrink-0 ${toneText[r.tone]}`}><Icon name={b.icon} className="h-3.5 w-3.5" /></span>
              <span className="min-w-0 flex-1">{r.text}</span>
              {r.item_id && <button onClick={() => onAskItem(r.item_id!)} className="shrink-0 text-[11px] font-semibold text-accent-ink opacity-0 transition group-hover:opacity-100 focus:opacity-100">Ask</button>}
            </li>
          ))}
        </ul>);
    case "places":
      return (
        <div className="grid grid-cols-2 gap-2">
          {b.rows.map((r, i) => (
            <div key={i} className="flex items-start gap-2 rounded-xl bg-sunken px-3 py-2">
              <Icon name="pin" className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[#2d6fb8]" />
              <div className="min-w-0"><div className="flex items-baseline justify-between gap-2 text-[13px] font-semibold"><span className="truncate">{r.place}</span>
                {r.value && <span className="shrink-0 text-xs tabular-nums text-muted">{r.value}</span>}</div>
                {r.note && <div className="text-[11.5px] leading-snug text-faint">{r.note}</div>}</div>
            </div>
          ))}
        </div>);
    case "competitors":
      return (
        <div className="space-y-1.5">
          {b.rows.map((r, i) => (
            <div key={i} className="flex items-center gap-2.5 rounded-xl bg-sunken px-3 py-2">
              <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-[#f4effb] text-[11px] font-bold text-[#7a5cc4]">{r.name.slice(0, 1).toUpperCase()}</span>
              <div className="min-w-0"><div className="truncate text-[13px] font-semibold">{r.name}</div>
                {r.note && <div className="text-[11.5px] leading-snug text-faint">{r.note}</div>}</div>
            </div>
          ))}
        </div>);
  }
}

/** The stage as pictures: verdict, a row of numbers, then blocks that look like their subject. */
export function StageViewBody({ view, items, onQuote }: { view: View; items: Item[]; onQuote: (i: Item) => void }) {
  const ask = (id: string) => { const it = items.find((x) => x.id === id); if (it) onQuote(it); };
  return (
    <div className="space-y-4" data-testid="stage-view">
      {view.verdict && <p className="text-[14.5px] leading-snug text-muted"><Rich text={view.verdict} /></p>}
      {view.kpis.length > 0 && (
        <div className="grid gap-2.5" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(9.5rem, 1fr))" }}>
          {view.kpis.map((k, i) => <Kpi key={i} k={k} />)}
        </div>
      )}
      {view.blocks.length > 0 && (
        <div className="gap-3.5 @2xl:columns-2 [&>*]:mb-3.5 [&>*]:break-inside-avoid">
          {view.blocks.map((b, i) => <Block key={i} b={b} onAskItem={ask} />)}
        </div>
      )}
      {view.kpis.length > 0 && (
        <div className="flex gap-3 text-[11px] text-faint">
          {[...new Set(view.kpis.map((k) => k.evidence))].map((l) => (
            <span key={l} className="inline-flex items-center gap-1.5"><LabelDot label={l} className="!h-2 !w-2" />{LABEL_NAME[l]}</span>
          ))}
        </div>
      )}
    </div>
  );
}

export function StageViewLoading() {
  return (
    <div className="space-y-4" aria-busy="true">
      <div className="flex items-center gap-2 text-[13px] text-faint">
        <span className="h-2 w-2 animate-pulse rounded-full bg-accent" />Writing this page from the latest findings…
      </div>
      <div className="grid gap-2.5" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(9.5rem, 1fr))" }}>
        {[0, 1, 2, 3].map((i) => <div key={i} className="h-[104px] animate-pulse rounded-2xl bg-frame/90" />)}
      </div>
      <div className="grid gap-3.5 @2xl:grid-cols-2">
        {[0, 1].map((i) => <div key={i} className="h-44 animate-pulse rounded-[18px] bg-sunken" />)}
      </div>
    </div>
  );
}
