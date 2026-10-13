import { useEffect, useState } from "react";
import { api } from "../api";
import type { Run } from "../types";
import { Button } from "./ui";

const SEV = { high: "text-rose-600 dark:text-rose-400", medium: "text-amber-700 dark:text-amber-300", low: "text-muted" } as const;

/** Stage 07: the daily account check. Plain comparisons, no Claude usage. */
export default function Rounds({ projectId, onAsk }: { projectId: string; onAsk: (text: string) => void }) {
  const [runs, setRuns] = useState<Run[] | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const load = () => api.runs(projectId).then(setRuns).catch((e) => setError(String(e.message ?? e)));
  useEffect(() => { setRuns(null); setError(""); load(); }, [projectId]);

  const runNow = async () => {
    setBusy(true); setError("");
    try { await api.accountCheck(projectId, true); await load(); } catch (e: any) { setError(String(e.message ?? e)); } finally { setBusy(false); }
  };
  const last = runs?.find((r) => r.kind === "account_check");
  return (
    <div className="space-y-2 rounded-xl border border-line bg-panel p-3 text-xs" data-testid="rounds">
      <div className="flex items-center justify-between gap-2">
        <span className="text-sm font-medium">Daily account check</span>
        <Button variant="outline" className="!px-2 !py-1 !text-xs" disabled={busy} onClick={runNow}>{busy ? "Checking…" : "Run now"}</Button>
      </div>
      {error && <div className="text-rose-600 dark:text-rose-400">{error}</div>}
      {!last ? (
        <div className="text-faint">No check yet. It needs Stage 01 set up with a customer ID. To run it every morning, run <code>scripts\schedule.ps1</code> once.</div>
      ) : (
        <div className="space-y-1.5">
          <div className={last.attention ? "font-medium text-amber-700 dark:text-amber-300" : "text-muted"}>
            {last.run_date} · {last.status === "failed" ? `failed: ${last.error}` : last.summary}
          </div>
          {(last.findings ?? []).map((f, i) => (
            <div key={i}><span className={`font-medium ${SEV[f.severity]}`}>{f.title}</span> <span className="text-muted">{f.detail}</span> <span className="text-faint">[{f.label}]</span></div>
          ))}
          {last.attention && <button className="text-accent hover:underline" onClick={() => onAsk("Look at today's account check and tell me what, if anything, I should do.")}>Ask the strategist about it</button>}
          {runs && runs.length > 1 && (
            <div className="border-t border-line pt-1.5 text-faint">
              {runs.slice(1, 6).map((r) => <div key={r.id}>{r.run_date} · {r.status === "failed" ? "failed" : r.summary}</div>)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
