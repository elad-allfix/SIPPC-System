import { useEffect, useState } from "react";
import { api } from "../api";
import type { Connectivity as State, ConnectionProfile, Verification } from "../types";
import { Button } from "./ui";

const field = "w-full rounded-lg border border-line bg-panel px-2.5 py-1.5 text-sm outline-none focus:border-accent";

const CHECK_TITLE: Record<string, string> = {
  profile: "Connection profile",
  pia_connected: "PIA connected",
  pia_public_ip: "PIA public IP",
  "pia_region (advisory)": "PIA region (advisory)",
  ip_echo: "Outside services agree on the IP",
  matches_pia: "IP matches PIA",
  country: "Country",
  "region (advisory)": "Region (advisory)",
  dolphin: "Dolphin Anty profile (advisory)",
};

const FIELDS: { key: keyof ConnectionProfile; label: string; hint: string }[] = [
  { key: "required_country", label: "Required country", hint: "Two letters, e.g. US" },
  { key: "required_region", label: "Expected region", hint: "Optional, e.g. Texas. Only a warning." },
  { key: "vpn_profile", label: "PIA region", hint: "Optional, as piactl names it, e.g. us-texas" },
  { key: "ads_customer_id", label: "Google Ads customer ID", hint: "123-456-7890" },
  { key: "login_customer_id", label: "Manager (MCC) ID", hint: "Only if you reach the account through a manager" },
  { key: "dolphin_profile_id", label: "Dolphin Anty profile ID", hint: "Optional, for browser sessions" },
];

function Mark({ ok }: { ok: boolean | null }) {
  const [c, t] = ok === true ? ["text-emerald-600 dark:text-emerald-400", "✓"] : ok === false ? ["text-rose-600 dark:text-rose-400", "✕"] : ["text-faint", "–"];
  return <span className={`w-4 shrink-0 text-center font-semibold ${c}`}>{t}</span>;
}

function Checklist({ v }: { v: Verification }) {
  return (
    <div className={`rounded-xl border p-3 ${v.ok ? "border-emerald-500/40" : "border-rose-500/40"}`} data-testid="route-result">
      <div className="mb-2 flex items-baseline justify-between gap-2">
        <span className="text-sm font-medium">{v.ok ? "Route verified, account access open" : "Blocked, account access closed"}</span>
        <span className="text-[11px] text-faint">{new Date(v.at).toLocaleTimeString()}</span>
      </div>
      <ul className="space-y-1 text-xs">
        {v.checks.map((c, i) => (
          <li key={i} className="flex gap-2"><Mark ok={c.ok} />
            <span><span className="text-fg">{CHECK_TITLE[c.name] ?? c.name}</span> <span className="text-muted">{c.detail}</span></span></li>
        ))}
      </ul>
      {v.public_ip && <div className="mt-2 text-[11px] text-faint">Seen as {v.public_ip} · {[v.country, v.region].filter(Boolean).join(" · ")}</div>}
    </div>
  );
}

const money = (n: number | null | undefined, cur?: string) => n == null ? "n/a" : `${n.toLocaleString()} ${cur ?? ""}`.trim();

function Snapshot({ s }: { s: NonNullable<State["snapshot"]> }) {
  if (s.status !== "done") {
    return <div className="rounded-xl border border-line p-3 text-xs text-muted">Last import {s.status}{s.error ? `: ${s.error}` : ""}</div>;
  }
  const m = s.summary;
  const terms = m.search_terms_without_conversions ?? {};
  return (
    <div className="space-y-2 rounded-xl border border-line bg-panel p-3 text-xs" data-testid="ads-snapshot">
      <div className="text-sm font-medium">{m.account ?? s.customer_id}</div>
      <div className="text-faint">{s.date_range} · imported {new Date(s.taken_at).toLocaleString()}</div>
      <dl className="grid grid-cols-2 gap-x-3 gap-y-1">
        {([["Cost", money(m.cost, m.currency)], ["Conversions", m.conversions], ["Cost / conv.", money(m.cost_per_conversion, m.currency)],
          ["Clicks", m.clicks], ["Campaigns live", m.campaigns_enabled], ["Auto-tagging", m.auto_tagging === false ? "off" : m.auto_tagging ? "on" : "n/a"]] as const)
          .map(([k, v]) => <div key={k}><dt className="text-faint">{k}</dt><dd className="tabular-nums">{String(v ?? "n/a")}</dd></div>)}
      </dl>
      {terms.count > 0 && <div className="text-muted">{terms.count} search terms spent {money(terms.cost, m.currency)} with no conversion in the window. Not proof of waste: ask the strategist.</div>}
      {m.conversion_actions?.length === 0 && <div className="text-rose-600 dark:text-rose-400">No conversion actions found.</div>}
    </div>
  );
}

export default function Connectivity({ projectId, onAsk }: { projectId: string; onAsk: (text: string) => void }) {
  const [state, setState] = useState<State | null>(null);
  const [form, setForm] = useState<Partial<ConnectionProfile>>({});
  const [busy, setBusy] = useState<"" | "save" | "verify" | "import">("");
  const [error, setError] = useState("");
  const [result, setResult] = useState<Verification | null>(null);

  const load = () => api.connectivity(projectId).then((s) => {
    setState(s);
    setForm(s.profile ?? { required_country: "" });
    setResult(s.profile?.last_result ?? null);
  }).catch((e) => setError(String(e.message ?? e)));
  useEffect(() => { setState(null); setError(""); load(); }, [projectId]);

  const run = async (kind: typeof busy, fn: () => Promise<unknown>) => {
    setBusy(kind); setError("");
    try { await fn(); } catch (e: any) { setError(String(e.message ?? e)); } finally { setBusy(""); }
  };
  const save = () => run("save", async () => {
    const body = Object.fromEntries(FIELDS.map((f) => [f.key, (form[f.key] as string | null) ?? ""]));
    await api.saveConnectivity(projectId, body);
    await load();
  });
  const verify = () => run("verify", async () => { setResult(await api.verifyRoute(projectId)); });
  const importAds = () => run("import", async () => { await api.importAds(projectId); await load(); });

  if (!state) return <div className="text-sm text-muted">{error || "Loading…"}</div>;
  const saved = !!state.profile;
  const dirty = FIELDS.some((f) => ((form[f.key] as string | null) ?? "") !== ((state.profile?.[f.key] as string | null) ?? ""));

  return (
    <div className="space-y-4 text-sm" data-testid="connectivity">
      <p className="text-xs text-muted">Before any Google Ads request, AllFix checks that PIA is connected and that outside services see the PIA IP in the required country. If any check fails, the request never leaves the machine. Public research does not use this route.</p>
      <div className="space-y-2">
        {FIELDS.map((f) => (
          <label key={f.key} className="block space-y-0.5">
            <span className="text-xs text-muted">{f.label}</span>
            <input className={field} value={(form[f.key] as string | null) ?? ""} placeholder={f.hint} name={f.key}
              onChange={(e) => setForm((x) => ({ ...x, [f.key]: e.target.value }))} />
          </label>
        ))}
        <Button variant="outline" disabled={!dirty || busy !== "" || !form.required_country} onClick={save}>{busy === "save" ? "Saving…" : saved ? "Save changes" : "Save profile"}</Button>
      </div>

      <div className="space-y-2 border-t border-line pt-4">
        <div className="flex flex-wrap gap-2">
          <Button variant="primary" className="whitespace-nowrap" disabled={!saved || dirty || busy !== ""} onClick={verify}>{busy === "verify" ? "Checking…" : "Verify route"}</Button>
          <Button variant="outline" disabled={!saved || dirty || busy !== "" || !state.ads_configured || !state.profile?.ads_customer_id}
            onClick={importAds} title={state.ads_configured ? "Read-only: last 90 days" : "Google Ads access is not set up yet"}>
            {busy === "import" ? "Importing…" : "Import account (read-only)"}</Button>
        </div>
        {!state.ads_configured && <p className="text-xs text-faint">Google Ads access is not set up on this machine. Run <code>python -m allfix ads-login</code> (see docs/GOOGLE_ADS_SETUP.md).</p>}
        {error && <p className="text-xs text-rose-600 dark:text-rose-400" data-testid="connectivity-error">{error}</p>}
        {result && <Checklist v={result} />}
      </div>

      {state.snapshot && (
        <div className="space-y-2 border-t border-line pt-4">
          <Snapshot s={state.snapshot} />
          {state.snapshot.status === "done" && <Button variant="outline" className="!text-xs" onClick={() => onAsk("Review the Google Ads account I just imported. Start with tracking and where the money goes.")}>Ask the strategist to review it</Button>}
        </div>
      )}
    </div>
  );
}
