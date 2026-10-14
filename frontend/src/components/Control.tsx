import { useEffect, useState } from "react";
import { api } from "../api";
import type { Item, Project, ProjectCard, Stage } from "../types";
import Rounds from "./Rounds";
import { KIND_TITLE } from "./ui";

const NEED: Record<string, { tag: string; color: string; ask: (t: string) => string }> = {
  do: { tag: "Do", color: "var(--accent-ink)", ask: (t) => /exports|account check/i.test(t)
    ? "I want to run the account check. Which Google Ads report exports should I attach, with which columns and date range? "
    : /website/i.test(t) ? "The website address is " : `${t}: ` },
  fix: { tag: "Fix", color: "var(--danger)", ask: (t) => `How do we fix "${t}"? ` },
  risk: { tag: "Risk", color: "var(--ev-unknown)", ask: (t) => `About the risk "${t}": ` },
  check: { tag: "Check", color: "var(--ev-estimate)", ask: (t) => `Score the forecast "${t}" against what happened: ` },
  answer: { tag: "Answer", color: "var(--ev-observed)", ask: (t) => `Answer to "${t}": ` },
};

/** Stage 07: what this project needs now, the plan's open actions, then the stages at a glance. */
export default function Control({ project, stages, onAsk, onSelectStage }: {
  project: Project; stages: Stage[]; onAsk: (text: string) => void; onSelectStage: (n: number) => void;
}) {
  const [card, setCard] = useState<ProjectCard | null>(null);
  const [actions, setActions] = useState<Item[]>([]);
  const [connected, setConnected] = useState(false);
  useEffect(() => {
    setCard(null); setActions([]);
    api.needs(project.id).then(setCard).catch(() => setCard(null));
    api.items(project.id).then((all) => setActions(all.filter((i) => i.status === "open" && (i.kind === "opportunity" || i.kind === "decision"))))
      .catch(() => setActions([]));
    api.connectivity(project.id).then((c) => setConnected(!!c.profile)).catch(() => setConnected(false));
  }, [project.id, project.updated_at]);

  const counts = project.stage_counts ?? {};
  const head = "mb-2 text-[11px] font-semibold uppercase tracking-[0.08em] text-faint";
  return (
    <div className="space-y-5" data-testid="control">
      <section>
        <h3 className={head}>Needs now</h3>
        {!card ? <div className="text-sm text-faint">Loading…</div> : card.needs.length === 0 ? (
          <div className="rounded-xl border border-dashed border-line px-3 py-4 text-center text-sm text-faint">
            {card.item_total ? "Nothing open needs you right now." : "Nothing saved yet. Start in the chat."}
          </div>
        ) : (
          <div className="space-y-1.5">
            {card.needs.map((n, i) => (
              <button key={i} onClick={() => onAsk(NEED[n.kind]?.ask(n.text) ?? n.text)} data-testid="control-need"
                className="flex w-full items-start gap-2 rounded-xl border border-line bg-panel p-2.5 text-left text-sm hover:border-accent">
                <span className="mt-0.5 w-12 shrink-0 text-[10px] font-bold uppercase tracking-[0.06em]" style={{ color: NEED[n.kind]?.color }}>
                  {NEED[n.kind]?.tag ?? n.kind}
                </span>
                <span className="min-w-0">{n.text}</span>
              </button>
            ))}
          </div>
        )}
      </section>

      {actions.length > 0 && (
        <section>
          <h3 className={head}>Open actions · {actions.length}</h3>
          <div className="space-y-1.5">
            {actions.map((a) => (
              <button key={a.id} onClick={() => onSelectStage(a.stage)}
                className="block w-full rounded-xl border border-line bg-panel p-2.5 text-left text-sm hover:border-accent">
                <span className="text-[10px] font-bold uppercase tracking-[0.06em] text-faint">{a.kind === "decision" ? "Decision" : "Move"}</span>
                <span className="block">{a.title}</span>
              </button>
            ))}
          </div>
        </section>
      )}

      {connected && <Rounds projectId={project.id} onAsk={onAsk} />}

      <section>
        <h3 className={head}>Stages</h3>
        <div className="space-y-1.5">
          {stages.filter((x) => x.n !== 7).map((x) => {
            const c = counts[String(x.n)] ?? {};
            const total = Object.values(c).reduce((a, b) => a + b, 0);
            return (
              <button key={x.n} onClick={() => onSelectStage(x.n)} className="block w-full rounded-xl border border-line bg-panel p-2.5 text-left hover:border-accent">
                <div className="flex justify-between text-sm"><span className="font-medium">{String(x.n).padStart(2, "0")} {x.title}</span><span className="tabular-nums text-muted">{total}</span></div>
                <div className="mt-0.5 text-xs text-faint">
                  {x.n === 2 ? `${project.facts?.length ?? 0} facts${total ? " · " : ""}` : ""}
                  {total === 0 ? (x.n === 2 ? "" : x.n === 1 ? (connected ? "Connection set up" : "Optional: live account connection") : "Nothing yet")
                    : Object.entries(c).map(([k, n]) => `${n} ${(KIND_TITLE[k] ?? k).toLowerCase()}`).join(" · ")}
                </div>
              </button>
            );
          })}
        </div>
      </section>
    </div>
  );
}
