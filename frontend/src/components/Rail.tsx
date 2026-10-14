import { useState } from "react";
import type { Health, Project, Stage } from "../types";

/** Short names for the seven stages; the full title and summary stay in the tooltip. */
const SHORT: Record<number, string> = {
  1: "Connection", 2: "Business", 3: "Market", 4: "Website & ads", 5: "Growth", 6: "Learning", 7: "Control",
};
export const stageName = (s: Stage) => SHORT[s.n] ?? s.title;

function stageTotal(p: Project | null, n: number): number {
  const c = p?.stage_counts?.[String(n)];
  return c ? Object.values(c).reduce((a, b) => a + b, 0) : 0;
}

interface TopProps {
  projects: Project[];
  project: Project | null;
  view: "overview" | "chat" | "knowledge";
  health: Health | null;
  onSelectProject: (id: string) => void;
  onNewProject: () => void;
  onKnowledge: () => void;
  /** One level up: project or library to the projects page, the projects page to the entrance. */
  onBack: () => void;
  onAllProjects: () => void;
}

/** Dark top bar: back, logo (all projects), project switcher, library, and one status dot for Claude. */
export function TopBar(p: TopProps) {
  const [open, setOpen] = useState(false);
  const back = p.view === "overview" ? "Back to the entrance" : p.view === "knowledge" ? "Close the library" : "All projects";
  return (
    <header className="flex items-center gap-3 px-1">
      <div className="flex w-[13.25rem] shrink-0 items-center gap-2 max-md:w-auto">
        <button onClick={p.onBack} aria-label={back} title={back} data-testid="home"
          className="grid h-9 w-9 place-items-center rounded-full border border-line text-faint hover:text-fg">←</button>
        <button onClick={p.onAllProjects} title="All projects" data-testid="logo" className="flex items-center gap-2.5 text-xl font-extrabold tracking-tight">
          <span className="h-6 w-6 rounded-[7px] shadow-[inset_0_1px_0_rgba(255,255,255,.35)]"
            style={{ background: "linear-gradient(145deg, var(--accent), #b86d0c)" }} />
          AllFix
        </button>
      </div>

      {p.view === "overview" ? <span className="text-sm font-semibold text-faint">All projects</span> : (
      <div className="relative min-w-0">
        <button onClick={() => setOpen((o) => !o)} data-testid="project-switcher"
          className="flex min-w-0 items-center gap-2 rounded-full border border-line bg-panel px-4 py-2 text-sm font-semibold hover:bg-sunken">
          <span className="truncate">{p.project?.name ?? "No project yet"}</span>
          <svg className="h-4 w-4 shrink-0 text-faint" viewBox="0 0 20 20" fill="currentColor"><path d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" /></svg>
        </button>
        {open && (
          <div className="absolute left-0 z-30 mt-2 max-h-80 w-72 overflow-auto rounded-2xl border border-line bg-panel p-1.5 shadow-2xl scroll-thin">
            <button onClick={() => { setOpen(false); p.onAllProjects(); }} data-testid="all-projects"
              className="mb-1 block w-full rounded-xl border-b border-line px-3 py-2 text-left text-sm font-semibold hover:bg-sunken">
              All projects
            </button>
            {p.projects.map((pr) => (
              <button key={pr.id} onClick={() => { setOpen(false); p.onSelectProject(pr.id); }}
                className={`block w-full truncate rounded-xl px-3 py-2 text-left text-sm hover:bg-sunken ${pr.id === p.project?.id ? "font-semibold text-accent" : ""}`}>
                {pr.name}
              </button>
            ))}
            <button onClick={() => { setOpen(false); p.onNewProject(); }}
              className="mt-1 block w-full rounded-xl px-3 py-2 text-left text-sm text-accent hover:bg-sunken">
              + New project
            </button>
          </div>
        )}
      </div>
      )}

      <div className="ml-auto flex items-center gap-3">
        <button onClick={p.onKnowledge}
          className={`rounded-full px-3.5 py-1.5 text-sm ${p.view === "knowledge" ? "bg-panel text-fg" : "text-faint hover:text-fg"}`}>
          {p.view === "knowledge" ? "← Close library" : "Library"}
        </button>
        {p.health && <Status h={p.health} />}
      </div>
    </header>
  );
}

/** One dot: green when Claude runs on the subscription, red if an API key would be billed. */
function Status({ h }: { h: Health }) {
  const src = h.subscription?.api_key_source;
  const win = h.subscription?.rate_limit?.unifiedWindows?.five_hour?.utilization;
  const bad = h.backend === "subscription" && !!src && src !== "none";
  const title = h.backend === "api" ? "Claude API key, billed per use"
    : bad ? `Claude Code reported an API key (${src}); AllFix will not run on it.`
    : `Claude subscription${typeof win === "number" ? ` · ${Math.round(win * 100)}% of the 5-hour limit used` : ""}`;
  const color = bad ? "var(--ev-unknown)" : "var(--ev-verified)";
  return (
    <span title={title} aria-label={title} data-testid="engine" className="mr-1 inline-block h-2.5 w-2.5 rounded-full"
      style={{ background: color, boxShadow: `0 0 0 4px color-mix(in srgb, ${color} 22%, transparent)` }} />
  );
}

interface StepProps {
  project: Project | null;
  stages: Stage[];
  stage: number;
  view: "overview" | "chat" | "knowledge";
  onSelectStage: (n: number) => void;
}

/** The seven steps as a numbered path. Steps with saved work show green; the open one glows. */
export function Steps(p: StepProps) {
  return (
    <nav aria-label="Steps" className="w-[13.25rem] shrink-0 max-md:w-full">
      <ol className="relative flex flex-col gap-0.5 py-2 max-md:flex-row max-md:overflow-x-auto max-md:py-0">
        <span aria-hidden className="absolute bottom-6 left-[1.1rem] top-6 w-px bg-line max-md:hidden" />
        {p.stages.map((s) => {
          const n = stageTotal(p.project, s.n);
          const active = p.view === "chat" && p.stage === s.n;
          return (
            <li key={s.n} className="max-md:shrink-0">
              <button onClick={() => p.onSelectStage(s.n)} title={`${s.title}: ${s.summary}`} data-testid={`stage-${s.n}`}
                className={`flex w-full items-center gap-3 rounded-xl py-2 pl-1 pr-2.5 text-left text-sm font-medium transition
                  ${active ? "bg-panel text-fg" : n > 0 ? "text-fg hover:bg-panel/60" : "text-faint hover:bg-panel/60 hover:text-fg"}`}>
                <span className={`relative z-10 grid h-7 w-7 shrink-0 place-items-center rounded-full border text-xs font-bold
                  ${active ? "step-glow border-accent bg-accent text-accent-fg" : n > 0 ? "border-[#2f5d4b] bg-frame text-[#7fd1ae]" : "border-line bg-frame"}`}>
                  {s.n}
                </span>
                <span className={`min-w-0 flex-1 truncate ${!active ? "max-md:hidden" : ""}`}>{stageName(s)}</span>
                {n > 0 && <span className="text-xs tabular-nums text-faint max-md:hidden">{n}</span>}
              </button>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
