import { useState } from "react";
import type { Item, Project, Stage } from "../types";
import Connectivity from "./Connectivity";
import Ledger from "./Ledger";
import Control from "./Control";
import { stageName } from "./Rail";
import { Button, ENTRY_PATH_TITLE, EvidenceScale, KIND_TITLE, LabelBadge, LabelDot, Markdown, hostOf } from "./ui";

interface Props {
  project: Project;
  stage: Stage | undefined;
  stages: Stage[];
  items: Item[];
  onQuote: (item: Item) => void;
  onStatus: (item: Item, status: string) => void;
  onSelectStage: (n: number) => void;
  onAsk: (text: string) => void;
}

function ItemCard({ item, onQuote, onStatus }: { item: Item; onQuote: (i: Item) => void; onStatus: (i: Item, s: string) => void }) {
  const [open, setOpen] = useState(false);
  const closed = ["refuted", "dropped", "superseded", "done"].includes(item.status);
  return (
    <div className={`rounded-2xl bg-sunken p-3.5 transition ${open ? "ring-1 ring-line" : "hover:ring-1 hover:ring-line"} ${closed ? "opacity-55" : ""}`} data-testid="item-card">
      <button onClick={() => setOpen((o) => !o)} className="flex w-full items-start gap-2.5 text-left">
        <LabelDot label={item.label} className="mt-1.5" />
        <span className={`text-sm font-semibold leading-snug ${closed ? "line-through decoration-faint" : ""}`}>{item.title}</span>
      </button>
      {open && (
        <div className="mt-3 space-y-3 border-t border-line pt-3">
          <div className="flex flex-wrap gap-x-3 gap-y-1 text-[11px] text-faint">
            <LabelBadge label={item.label} />
            {item.confidence && <span>{item.confidence} confidence</span>}
            {item.status !== "open" && <span>{item.status}</span>}
          </div>
          <div className="text-[13px]"><Markdown>{item.body}</Markdown></div>
          {item.data && Object.keys(item.data).length > 0 && (
            <dl className="space-y-1 text-xs">
              {Object.entries(item.data).map(([k, v]) => (
                <div key={k}><dt className="inline text-faint">{k.replace(/_/g, " ")}: </dt>
                  <dd className="inline text-muted">{Array.isArray(v) ? v.join(", ") : typeof v === "object" ? JSON.stringify(v) : String(v)}</dd></div>
              ))}
            </dl>
          )}
          {item.sources?.length > 0 && (
            <ul className="space-y-0.5 text-xs">
              {item.sources.map((s, i) => (
                <li key={i} className="truncate text-muted">
                  {s.url ? <a href={s.url} target="_blank" rel="noreferrer noopener" className="text-accent-ink hover:underline">{s.title || hostOf(s.url)}</a>
                    : s.kb ? <span>Knowledge {s.kb}</span> : null}
                  {s.note ? <span>{s.url || s.kb ? " · " : ""}{s.note}</span> : null}
                </li>
              ))}
            </ul>
          )}
          <div className="flex flex-wrap gap-1.5">
            {item.status === "open" && <>
              <Button variant="primary" className="!px-3 !py-1 !text-xs" onClick={() => onStatus(item, "confirmed")}>Keep</Button>
              <Button variant="outline" className="!px-3 !py-1 !text-xs" onClick={() => onStatus(item, "refuted")}>Wrong</Button>
              <Button variant="outline" className="!px-3 !py-1 !text-xs" onClick={() => onStatus(item, "dropped")}>Drop</Button>
            </>}
            <Button variant="outline" className="!px-3 !py-1 !text-xs" onClick={() => onQuote(item)}>Ask</Button>
            {item.status !== "open" && item.status !== "superseded" &&
              <Button variant="outline" className="!px-3 !py-1 !text-xs" onClick={() => onStatus(item, "open")}>Reopen</Button>}
          </div>
        </div>
      )}
    </div>
  );
}

function Grouped({ items, ...rest }: { items: Item[]; onQuote: (i: Item) => void; onStatus: (i: Item, s: string) => void }) {
  const groups = new Map<string, Item[]>();
  for (const it of items) groups.set(it.kind, [...(groups.get(it.kind) ?? []), it]);
  return (
    <div className="space-y-5">
      {[...groups.entries()].map(([kind, list]) => (
        <div key={kind}>
          <h3 className="mb-2 flex justify-between text-xs font-semibold text-faint"><span>{KIND_TITLE[kind] ?? kind}</span><span className="tabular-nums">{list.length}</span></h3>
          <div className="space-y-2">{list.map((i) => <ItemCard key={i.id} item={i} {...rest} />)}</div>
        </div>
      ))}
    </div>
  );
}

function Empty({ children }: { children: React.ReactNode }) {
  return <div className="rounded-2xl border border-dashed border-line px-4 py-6 text-center text-sm text-faint">{children}</div>;
}

export default function StagePanel(p: Props) {
  const s = p.stage;
  if (!s) return null;
  const pr = p.project;
  const actions = { onQuote: p.onQuote, onStatus: p.onStatus };

  let body: React.ReactNode;
  if (s.n === 1) {
    body = (
      <div className="space-y-5">
        {p.items.length > 0 && <Grouped items={p.items} {...actions} />}
        <div className="rounded-2xl border border-line p-3 text-sm text-muted">
          Live account access is optional. Today the account is read from report exports: use Account check in the chat.
        </div>
        <Connectivity projectId={pr.id} onAsk={p.onAsk} />
      </div>
    );
  } else if (s.n === 2) {
    const facts = pr.facts ?? [];
    body = (
      <div className="space-y-5">
        <dl className="space-y-2 text-sm">
          {([
            ["Entry path", ENTRY_PATH_TITLE[pr.entry_path]],
            ["Objective", pr.objective || "Not set"],
            ["Objective type", pr.objective_type],
            ["Market", [pr.country, pr.region, pr.language].filter(Boolean).join(" · ") || "Not set"],
            ["Website", pr.website_url || "None"],
          ] as const).map(([k, v]) => (
            <div key={k}><dt className="text-xs text-faint">{k}</dt><dd className="break-words">{v}</dd></div>
          ))}
        </dl>
        <div>
          <h3 className="mb-2 text-[11px] font-medium uppercase tracking-wider text-faint">Business facts · {facts.length}</h3>
          {facts.length === 0 ? <Empty>No facts recorded yet. Tell the strategist what kind of business this is, what a conversion is and what it is worth, margins, close rate and capacity.</Empty> : (
            <div className="space-y-1.5">
              {facts.map((f) => (
                <div key={f.key} className="rounded-lg border border-line bg-panel px-3 py-2">
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-xs text-faint">{f.key.replace(/_/g, " ")}</span><LabelBadge label={f.label} />
                  </div>
                  <div className="text-sm">{f.value}</div>
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate text-[11px] text-faint">{f.source}</span>
                    <button onClick={() => p.onAsk(`Correct the business fact with key "${f.key}" (now ${f.value}, ${f.label}): it should be `)}
                      className="shrink-0 text-[11px] text-accent-ink hover:underline" data-testid="correct-fact">Correct</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        {p.items.length > 0 && <Grouped items={p.items} {...actions} />}
      </div>
    );
  } else if (s.n === 6) {
    body = (
      <div className="space-y-5">
        <Ledger items={p.items} onAsk={p.onAsk} />
        {p.items.length === 0 ? <Empty>Nothing saved here yet. Decisions, forecasts and experiments land here.</Empty>
          : <Grouped items={p.items} {...actions} />}
      </div>
    );
  } else if (s.n === 7) {
    body = <Control project={pr} stages={p.stages} onAsk={p.onAsk} onSelectStage={p.onSelectStage} />;
  } else {
    body = p.items.length === 0 ? <Empty>{s.n === 4 && pr.entry_path === "ads_account"
      ? "Start here: press Account check in the chat and attach the account's report exports (campaigns, search terms, keywords, ads, change history)."
      : "Findings appear here as the strategist works."}</Empty>
      : <Grouped items={p.items} {...actions} />;
  }

  const showScale = s.n !== 7 && p.items.length > 0;
  return (
    <aside className="sheet flex w-[21rem] shrink-0 flex-col max-xl:w-[18rem] max-md:w-full">
      <div className="space-y-3 px-5 pb-3 pt-5" title={s.summary}>
        <h2 className="flex items-baseline justify-between text-lg font-bold tracking-tight">
          <span>{stageName(s)}</span>
          {p.items.length > 0 && <span className="text-sm font-medium tabular-nums text-faint">{p.items.length}</span>}
        </h2>
        {showScale && <EvidenceScale labels={p.items.map((i) => i.label)} />}
      </div>
      <div className="flex-1 overflow-auto px-3 pb-4 scroll-thin" data-testid="stage-panel">{body}</div>
    </aside>
  );
}
