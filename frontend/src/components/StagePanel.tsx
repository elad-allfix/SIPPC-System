import { useState } from "react";
import type { Item, Project, Stage } from "../types";
import { Button, ENTRY_PATH_TITLE, KIND_TITLE, LabelBadge, Markdown, hostOf } from "./ui";

interface Props {
  project: Project;
  stage: Stage | undefined;
  stages: Stage[];
  items: Item[];
  onQuote: (item: Item) => void;
  onStatus: (item: Item, status: string) => void;
  onSelectStage: (n: number) => void;
}

function ItemCard({ item, onQuote, onStatus }: { item: Item; onQuote: (i: Item) => void; onStatus: (i: Item, s: string) => void }) {
  const [open, setOpen] = useState(false);
  const closed = ["refuted", "dropped", "superseded", "done"].includes(item.status);
  return (
    <div className={`rounded-xl border border-line bg-panel p-3 ${closed ? "opacity-60" : ""}`} data-testid="item-card">
      <button onClick={() => setOpen((o) => !o)} className="block w-full text-left">
        <div className="flex items-start justify-between gap-2">
          <span className="text-sm font-medium leading-snug">{item.title}</span>
          <LabelBadge label={item.label} />
        </div>
        <div className="mt-1 flex gap-2 text-[11px] text-faint">
          {item.confidence && <span>{item.confidence} confidence</span>}
          {item.status !== "open" && <span>· {item.status}</span>}
          {item.sources?.length > 0 && <span>· {item.sources.length} source{item.sources.length > 1 ? "s" : ""}</span>}
        </div>
      </button>
      {open && (
        <div className="mt-3 space-y-3 border-t border-line pt-3">
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
                  {s.url ? <a href={s.url} target="_blank" rel="noreferrer noopener" className="text-accent hover:underline">{s.title || hostOf(s.url)}</a>
                    : s.kb ? <span>Knowledge {s.kb}</span> : null}
                  {s.note ? <span>{s.url || s.kb ? " · " : ""}{s.note}</span> : null}
                </li>
              ))}
            </ul>
          )}
          <div className="flex flex-wrap gap-1">
            <Button variant="outline" className="!px-2 !py-1 !text-xs" onClick={() => onQuote(item)}>Ask about this</Button>
            {item.status === "open" && <>
              <Button className="!px-2 !py-1 !text-xs" onClick={() => onStatus(item, "confirmed")}>Confirm</Button>
              <Button className="!px-2 !py-1 !text-xs" onClick={() => onStatus(item, "refuted")}>Refute</Button>
              <Button className="!px-2 !py-1 !text-xs" onClick={() => onStatus(item, "dropped")}>Drop</Button>
            </>}
            {item.status !== "open" && item.status !== "superseded" &&
              <Button className="!px-2 !py-1 !text-xs" onClick={() => onStatus(item, "open")}>Reopen</Button>}
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
          <h3 className="mb-2 text-[11px] font-medium uppercase tracking-wider text-faint">{KIND_TITLE[kind] ?? kind} · {list.length}</h3>
          <div className="space-y-2">{list.map((i) => <ItemCard key={i.id} item={i} {...rest} />)}</div>
        </div>
      ))}
    </div>
  );
}

function Empty({ children }: { children: React.ReactNode }) {
  return <div className="rounded-xl border border-dashed border-line px-4 py-6 text-center text-sm text-muted">{children}</div>;
}

export default function StagePanel(p: Props) {
  const s = p.stage;
  if (!s) return null;
  const pr = p.project;
  const actions = { onQuote: p.onQuote, onStatus: p.onStatus };

  let body: React.ReactNode;
  if (s.n === 1) {
    body = (
      <div className="space-y-3 text-sm text-muted">
        <Empty>Not built yet. This is Phase 5 of the roadmap.</Empty>
        <p>Before AllFix touches a Google Ads account it will check, every time, that traffic leaves through the expected PIA route and that the browser session runs in the expected Dolphin profile. If the check fails, account access stays closed.</p>
        <p>Public market research does not need this stage and is never blocked by it.</p>
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
          {facts.length === 0 ? <Empty>No facts recorded yet. Tell the strategist about margins, order value, close rate and capacity.</Empty> : (
            <div className="space-y-1.5">
              {facts.map((f) => (
                <div key={f.key} className="rounded-lg border border-line bg-panel px-3 py-2">
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-xs text-faint">{f.key.replace(/_/g, " ")}</span><LabelBadge label={f.label} />
                  </div>
                  <div className="text-sm">{f.value}</div>
                  {f.source && <div className="text-[11px] text-faint">{f.source}</div>}
                </div>
              ))}
            </div>
          )}
        </div>
        {p.items.length > 0 && <Grouped items={p.items} {...actions} />}
      </div>
    );
  } else if (s.n === 7) {
    const counts = pr.stage_counts ?? {};
    body = (
      <div className="space-y-2">
        {p.stages.filter((x) => x.n !== 7).map((x) => {
          const c = counts[String(x.n)] ?? {};
          const total = Object.values(c).reduce((a, b) => a + b, 0);
          return (
            <button key={x.n} onClick={() => p.onSelectStage(x.n)} className="block w-full rounded-xl border border-line bg-panel p-3 text-left hover:border-accent">
              <div className="flex justify-between text-sm"><span className="font-medium">{String(x.n).padStart(2, "0")} {x.title}</span><span className="tabular-nums text-muted">{total}</span></div>
              <div className="mt-1 text-xs text-faint">
                {total === 0 ? (x.n === 1 ? "Phase 5, not built yet" : x.n === 2 ? `${pr.facts?.length ?? 0} facts` : "Nothing yet")
                  : Object.entries(c).map(([k, n]) => `${n} ${(KIND_TITLE[k] ?? k).toLowerCase()}`).join(" · ")}
              </div>
            </button>
          );
        })}
      </div>
    );
  } else {
    body = p.items.length === 0 ? <Empty>Nothing saved here yet. The strategist saves findings as it works.</Empty>
      : <Grouped items={p.items} {...actions} />;
  }

  return (
    <aside className="flex h-full w-[22rem] shrink-0 flex-col border-l border-line bg-bg">
      <div className="border-b border-line px-5 py-3">
        <div className="text-xs text-faint">Stage {String(s.n).padStart(2, "0")}</div>
        <div className="text-sm font-medium">{s.title}</div>
        <div className="mt-0.5 text-xs text-muted">{s.summary}</div>
      </div>
      <div className="flex-1 overflow-auto p-4 scroll-thin" data-testid="stage-panel">{body}</div>
    </aside>
  );
}
