import { useEffect, useRef, useState } from "react";
import type { EntryPath, ObjectiveType, Project } from "../types";

/** Three tilted amber orbits with a travelling light each; `dim` for the setup screens. */
function Orbits({ dim = false }: { dim?: boolean }) {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const c = ref.current;
    if (!c) return;
    const ctx = c.getContext("2d");
    if (!ctx) return;
    const reduce = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    const amber = (a: number) => `rgba(224,148,34,${a})`;
    let raf = 0;
    const size = () => {
      const d = Math.min(window.devicePixelRatio || 1, 2);
      c.width = c.clientWidth * d; c.height = c.clientHeight * d;
      ctx.setTransform(d, 0, 0, d, 0, 0);
    };
    const draw = (t: number) => {
      const w = c.clientWidth, h = c.clientHeight, cx = w / 2, cy = h / 2, R = Math.min(w, h) * 0.36;
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < 3; i++) {
        const r = R * (1 + i * 0.22);
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(i * 1.05 + t * 0.00012 * (i + 1));
        ctx.scale(1, 0.32 + i * 0.1);
        ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2);
        ctx.strokeStyle = amber(dim ? 0.08 : 0.16 - i * 0.03); ctx.lineWidth = 1.2; ctx.stroke();
        const a = t * 0.0006 * (i % 2 ? -1 : 1) + i;
        ctx.beginPath(); ctx.arc(Math.cos(a) * r, Math.sin(a) * r, dim ? 2 : 3.2, 0, Math.PI * 2);
        ctx.fillStyle = amber(dim ? 0.4 : 0.95); ctx.shadowColor = amber(1); ctx.shadowBlur = 16; ctx.fill();
        ctx.restore();
      }
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 1.2);
      g.addColorStop(0, amber(dim ? 0.05 : 0.12)); g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
      if (!reduce) raf = requestAnimationFrame(draw);
    };
    size();
    const onResize = () => { size(); if (reduce) draw(4000); };
    window.addEventListener("resize", onResize);
    raf = requestAnimationFrame(reduce ? () => draw(4000) : draw);
    return () => { cancelAnimationFrame(raf); window.removeEventListener("resize", onResize); };
  }, [dim]);
  return <canvas ref={ref} aria-hidden className="pointer-events-none absolute inset-0 h-full w-full" />;
}

/** The front door: the name, one line, one button; then the choice between a new project and
 * the dashboard (the projects already there). */
export function Entrance({ projects, onNew, onDashboard }: {
  projects: Project[]; onNew: () => void; onDashboard: () => void;
}) {
  const [choosing, setChoosing] = useState(false);
  const latest = projects[0];
  return (
    <div className="frame relative grid h-full place-items-center overflow-auto bg-[#0a0b0d] px-4 text-center text-fg">
      <Orbits dim={choosing} />
      {!choosing ? (
        <div className="relative z-10 flex flex-col items-center gap-6">
          <div className="font-mono text-[11px] uppercase tracking-[0.32em] text-faint">Intelligence PPC System</div>
          <h1 className="text-[clamp(56px,11vw,128px)] font-extrabold leading-[0.9] tracking-[-0.04em]">
            AllFix<span className="text-accent">.</span>
          </h1>
          <div className="text-[15px] text-faint">Every click, accounted for.</div>
          <button autoFocus onClick={() => setChoosing(true)} className="cta mt-2" data-testid="enter">Enter</button>
        </div>
      ) : (
        <div className="relative z-10 flex w-full max-w-[760px] flex-col items-center gap-8 py-12">
          <div className="flex items-center gap-2.5 text-xl font-extrabold tracking-tight">
            <span className="h-6 w-6 rounded-[7px] shadow-[inset_0_1px_0_rgba(255,255,255,.35)]"
              style={{ background: "linear-gradient(145deg, var(--accent), #b86d0c)" }} />
            AllFix
          </div>
          <div className="grid w-full gap-3 sm:grid-cols-2">
            <button autoFocus onClick={onNew} data-testid="choose-new"
              className="group flex min-h-56 flex-col justify-between rounded-3xl border border-accent bg-[#1c160d] p-7 text-left transition hover:-translate-y-0.5 hover:shadow-[0_0_50px_rgba(224,148,34,.25)]">
              <span className="step-glow grid h-12 w-12 place-items-center rounded-full bg-accent text-2xl font-bold text-accent-fg">+</span>
              <span>
                <b className="block text-2xl font-bold tracking-[-0.03em]">New project</b>
                <span className="mt-1 block text-sm text-faint">Four quick questions</span>
              </span>
            </button>
            <button onClick={onDashboard} disabled={!latest} data-testid="choose-dashboard"
              className="flex min-h-56 flex-col justify-between rounded-3xl border border-line bg-panel p-7 text-left transition enabled:hover:-translate-y-0.5 enabled:hover:border-faint disabled:opacity-50">
              <span className="grid h-12 w-12 place-items-center rounded-full border border-line font-mono text-sm text-faint">
                {projects.length}
              </span>
              <span>
                <b className="block text-2xl font-bold tracking-[-0.03em]">Dashboard</b>
                <span className="mt-1 block truncate text-sm text-faint">
                  {latest ? `${projects.length === 1 ? "1 project" : `${projects.length} projects`} · ${latest.name}` : "No projects yet"}
                </span>
              </span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

const PATHS: { v: EntryPath; title: string; help: string }[] = [
  { v: "new_niche", title: "New niche", help: "Nothing live yet" },
  { v: "website", title: "Website", help: "Site, no ads" },
  { v: "ads_account", title: "Ads account", help: "Already running" },
];
const GOALS: { v: ObjectiveType; title: string }[] = [
  { v: "profit", title: "Profit" }, { v: "leads", title: "Leads" }, { v: "sales", title: "Sales" },
  { v: "traffic", title: "Traffic" }, { v: "unknown", title: "Not sure" },
];
const input = "w-full rounded-[14px] border border-line bg-panel px-4 py-3.5 text-[15px] outline-none placeholder:text-[#5b5e67] focus:border-accent";

/** New project as four short full-screen questions instead of a form. */
export function Setup({ onCreate, onCancel, canCancel }: {
  onCreate: (p: Partial<Project>) => Promise<void>; onCancel: () => void; canCancel: boolean;
}) {
  const [step, setStep] = useState(0);
  const [f, setF] = useState<Partial<Project>>({ entry_path: "new_niche", objective_type: "profit" });
  const [err, setErr] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const set = (k: keyof Project, v: string) => setF((o) => ({ ...o, [k]: v }));
  const last = 3;

  const next = async () => {
    setErr(null);
    if (step === 0 && !f.name?.trim()) { setErr("Name the business first."); return; }
    if (step < last) { setStep(step + 1); return; }
    setSaving(true);
    try {
      const clean = Object.fromEntries(Object.entries(f).map(([k, v]) => [k, typeof v === "string" && v.trim() === "" ? null : v]));
      await onCreate(clean as Partial<Project>);
    } catch (e) { setErr(String(e)); } finally { setSaving(false); }
  };
  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !(e.target instanceof HTMLTextAreaElement)) { e.preventDefault(); next(); }
  };

  const titles = ["What's the business?", "Where are we starting from?", "Where are the customers?", "What counts as a win?"];
  return (
    <div className="frame relative flex h-full items-center justify-center overflow-auto bg-[#0a0b0d] px-4 text-fg" data-testid="new-project" onKeyDown={onKey}>
      <Orbits dim />
      {canCancel && (
        <button onClick={onCancel} aria-label="Close" className="absolute right-5 top-5 z-20 grid h-10 w-10 place-items-center rounded-full border border-line text-faint hover:text-fg">×</button>
      )}
      <div className="relative z-10 flex w-full max-w-[640px] flex-col gap-6 py-12">
        <div className="flex gap-1.5" aria-hidden>
          {[0, 1, 2, 3].map((i) => <i key={i} className={`h-1 w-6 rounded-sm ${i <= step ? "bg-accent" : "bg-line"}`} />)}
        </div>
        <div className="font-mono text-xs tracking-[0.2em] text-accent">0{step + 1} / 04</div>
        <h2 className="text-[clamp(28px,4.4vw,44px)] font-bold leading-[1.08] tracking-[-0.035em]">{titles[step]}</h2>

        {step === 0 && (
          <input autoFocus className={`${input} !rounded-[18px] !px-5 !py-4 !text-[22px]`} value={f.name ?? ""} name="name"
            onChange={(e) => set("name", e.target.value)} placeholder="Emergency plumbing, Austin" />
        )}

        {step === 1 && (
          <div className="space-y-3">
            <div className="grid gap-2.5 sm:grid-cols-3">
              {PATHS.map((p, i) => {
                const sel = f.entry_path === p.v;
                return (
                  <button key={p.v} onClick={() => set("entry_path", p.v)} aria-pressed={sel}
                    className={`flex flex-col gap-2.5 rounded-2xl border p-4 text-left transition ${sel ? "border-accent bg-[#221a0e]" : "border-line bg-panel hover:border-faint"}`}>
                    <i className={`grid h-[30px] w-[30px] place-items-center rounded-[9px] border font-mono text-xs not-italic ${sel ? "border-accent bg-accent text-accent-fg" : "border-line text-faint"}`}>0{i + 1}</i>
                    <b className="text-[14.5px] font-semibold">{p.title}</b>
                    <span className="text-[12.5px] text-faint">{p.help}</span>
                  </button>
                );
              })}
            </div>
            {f.entry_path !== "new_niche" && (
              <input className={input} value={f.website_url ?? ""} onChange={(e) => set("website_url", e.target.value)} placeholder="Website, https://" />
            )}
          </div>
        )}

        {step === 2 && (
          <div className="grid gap-3 sm:grid-cols-3">
            <input autoFocus className={input} value={f.country ?? ""} onChange={(e) => set("country", e.target.value)} placeholder="Country" aria-label="Country" />
            <input className={input} value={f.region ?? ""} onChange={(e) => set("region", e.target.value)} placeholder="City (optional)" aria-label="City" />
            <input className={input} value={f.language ?? ""} onChange={(e) => set("language", e.target.value)} placeholder="Language" aria-label="Language" />
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <div className="flex flex-wrap gap-2">
              {GOALS.map((g) => {
                const sel = f.objective_type === g.v;
                return (
                  <button key={g.v} onClick={() => set("objective_type", g.v)} aria-pressed={sel}
                    className={`rounded-full border px-4 py-2.5 text-sm transition ${sel ? "border-accent bg-[#221a0e] text-fg" : "border-line text-faint hover:text-fg"}`}>
                    {g.title}
                  </button>
                );
              })}
            </div>
            <textarea rows={2} className={input} value={f.objective ?? ""} onChange={(e) => set("objective", e.target.value)}
              placeholder="In your words (optional): about 40 booked jobs a month" />
          </div>
        )}

        {err && <div className="text-sm text-[#f0a35a]">{err}</div>}
        <div className="flex items-center justify-between gap-3">
          {step > 0 ? <button onClick={() => setStep(step - 1)} className="rounded-full border border-line px-5 py-3 text-faint hover:text-fg">Back</button> : <span />}
          <button onClick={next} disabled={saving} className="cta">{step < last ? "Continue" : saving ? "Starting…" : "Start research"}</button>
        </div>
      </div>
    </div>
  );
}
