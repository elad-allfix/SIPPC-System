import { useState } from "react";
import type { Project, Stage } from "../types";
import { ENTRY_PATH_TITLE } from "./ui";

interface Props {
  projects: Project[];
  project: Project | null;
  stages: Stage[];
  stage: number;
  view: "chat" | "knowledge";
  kbCount: number | null;
  dark: boolean;
  onSelectProject: (id: string) => void;
  onNewProject: () => void;
  onSelectStage: (n: number) => void;
  onKnowledge: () => void;
  onToggleTheme: () => void;
}

function stageTotal(p: Project | null, n: number): number {
  const c = p?.stage_counts?.[String(n)];
  return c ? Object.values(c).reduce((a, b) => a + b, 0) : 0;
}

export default function Rail(p: Props) {
  const [open, setOpen] = useState(false);
  return (
    <aside className="flex h-full w-64 shrink-0 flex-col border-r border-line bg-panel">
      <div className="flex items-center gap-2 px-4 pt-4 pb-3">
        <div className="grid h-7 w-7 place-items-center rounded-lg bg-accent text-sm font-bold text-accent-fg">A</div>
        <span className="font-semibold tracking-tight">AllFix</span>
      </div>

      <div className="relative px-3">
        <button onClick={() => setOpen((o) => !o)} data-testid="project-switcher"
          className="flex w-full items-center justify-between rounded-lg border border-line px-3 py-2 text-left hover:bg-sunken">
          <span className="min-w-0">
            <span className="block truncate text-sm font-medium">{p.project?.name ?? "No project yet"}</span>
            {p.project && <span className="block truncate text-xs text-muted">{ENTRY_PATH_TITLE[p.project.entry_path]}{p.project.country ? ` · ${p.project.country}` : ""}</span>}
          </span>
          <svg className="h-4 w-4 shrink-0 text-faint" viewBox="0 0 20 20" fill="currentColor"><path d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" /></svg>
        </button>
        {open && (
          <div className="absolute left-3 right-3 z-20 mt-1 max-h-80 overflow-auto rounded-lg border border-line bg-panel p-1 shadow-lg scroll-thin">
            {p.projects.map((pr) => (
              <button key={pr.id} onClick={() => { setOpen(false); p.onSelectProject(pr.id); }}
                className={`block w-full truncate rounded-md px-2.5 py-1.5 text-left text-sm hover:bg-sunken ${pr.id === p.project?.id ? "font-medium text-accent" : ""}`}>
                {pr.name}
              </button>
            ))}
            <button onClick={() => { setOpen(false); p.onNewProject(); }}
              className="mt-1 block w-full rounded-md border-t border-line px-2.5 py-1.5 text-left text-sm text-accent hover:bg-sunken">
              + New project
            </button>
          </div>
        )}
      </div>

      <nav className="mt-5 flex-1 overflow-auto px-2 scroll-thin">
        <div className="px-2 pb-1.5 text-[11px] font-medium uppercase tracking-wider text-faint">Stages</div>
        {p.stages.map((s) => {
          const n = stageTotal(p.project, s.n);
          const active = p.view === "chat" && p.stage === s.n;
          return (
            <button key={s.n} onClick={() => p.onSelectStage(s.n)} title={s.summary} data-testid={`stage-${s.n}`}
              className={`group flex w-full items-center gap-2.5 rounded-lg px-2 py-1.5 text-left text-sm ${active ? "bg-accent-soft text-fg" : "text-muted hover:bg-sunken hover:text-fg"}`}>
              <span className={`w-5 text-xs tabular-nums ${active ? "text-accent" : "text-faint"}`}>{String(s.n).padStart(2, "0")}</span>
              <span className="min-w-0 flex-1 truncate">{s.title}</span>
              {n > 0 ? <span className="text-xs tabular-nums text-muted">{n}</span>
                : <span className="h-1.5 w-1.5 rounded-full bg-line" />}
            </button>
          );
        })}
      </nav>

      <div className="border-t border-line p-2">
        <button onClick={p.onKnowledge}
          className={`flex w-full items-center justify-between rounded-lg px-2 py-1.5 text-sm ${p.view === "knowledge" ? "bg-accent-soft" : "text-muted hover:bg-sunken hover:text-fg"}`}>
          <span>Knowledge base</span>
          {p.kbCount !== null && <span className="text-xs tabular-nums text-faint">{p.kbCount}</span>}
        </button>
        <button onClick={p.onToggleTheme} className="flex w-full items-center rounded-lg px-2 py-1.5 text-sm text-muted hover:bg-sunken hover:text-fg">
          {p.dark ? "Light theme" : "Dark theme"}
        </button>
      </div>
    </aside>
  );
}
