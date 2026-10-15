import { useState } from "react";

const ICON = { width: 15, height: 15, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2,
  strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
export function TrashIcon() {
  return <svg {...ICON}><path d="M3 6h18" /><path d="M8 6V4h8v2" /><path d="M19 6l-1 14H6L5 6" /><path d="M10 11v6M14 11v6" /></svg>;
}

/** A small bin icon that asks once ("Delete this project?") and then deletes. The project is hidden
 *  from AllFix, not wiped: its data stays in the database so a mistake can still be undone by hand. */
export function DeleteProject({ name, onDelete, className = "", align = "right" }: {
  name: string; onDelete: () => Promise<void>; className?: string; align?: "left" | "right";
}) {
  const [asking, setAsking] = useState(false);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const stop = (e: React.SyntheticEvent) => e.stopPropagation();
  const go = async () => {
    setBusy(true); setErr(null);
    try { await onDelete(); setAsking(false); } catch (e) { setErr(String(e)); } finally { setBusy(false); }
  };
  return (
    <div className="relative" onClick={stop} onKeyDown={stop}>
      <button onClick={() => setAsking((a) => !a)} aria-label="Delete project" title="Delete project" data-testid="trash"
        className={`grid place-items-center rounded-md p-1 text-faint transition hover:text-[#f07a5f] ${className}`}>
        <TrashIcon />
      </button>
      {asking && (
        <div className={`frame absolute top-full z-40 mt-2 w-64 rounded-2xl bg-[#17181c] p-4 text-left text-fg shadow-[0_24px_60px_-20px_rgba(0,0,0,.85)] ring-1 ring-white/10 ${align === "right" ? "right-0" : "left-0"}`}
          data-testid="delete-confirm">
          <div className="text-sm font-semibold leading-snug">Delete “{name}”?</div>
          <div className="mt-1 text-xs text-faint">It disappears from AllFix.</div>
          {err && <div className="mt-2 text-xs text-danger">{err}</div>}
          <div className="mt-3 flex gap-2">
            <button onClick={go} disabled={busy} data-testid="delete-yes"
              className="rounded-full bg-[#e2553a] px-4 py-1.5 text-xs font-bold text-white disabled:opacity-60">{busy ? "Deleting…" : "Delete"}</button>
            <button onClick={() => setAsking(false)} className="rounded-full px-3 py-1.5 text-xs text-faint hover:text-fg">Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}
