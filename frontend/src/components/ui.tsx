import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Label } from "../types";

const LABEL_STYLE: Record<Label, string> = {
  verified: "bg-emerald-500/12 text-emerald-700 dark:text-emerald-300 ring-emerald-500/25",
  observed: "bg-sky-500/12 text-sky-700 dark:text-sky-300 ring-sky-500/25",
  estimate: "bg-amber-500/12 text-amber-700 dark:text-amber-300 ring-amber-500/25",
  assumption: "bg-zinc-500/12 text-zinc-700 dark:text-zinc-300 ring-zinc-500/25",
  hypothesis: "bg-violet-500/12 text-violet-700 dark:text-violet-300 ring-violet-500/25",
  unknown: "bg-rose-500/12 text-rose-700 dark:text-rose-300 ring-rose-500/25",
};

export const LABEL_HELP: Record<Label, string> = {
  verified: "Checked against a primary source",
  observed: "Seen directly (a page, a results page, a tool output)",
  estimate: "A number derived from evidence, with a range",
  assumption: "Taken as given for planning; not checked",
  hypothesis: "A testable idea",
  unknown: "Not known yet",
};

export function LabelBadge({ label }: { label: Label }) {
  return (
    <span title={LABEL_HELP[label]}
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium ring-1 ring-inset ${LABEL_STYLE[label] ?? LABEL_STYLE.unknown}`}>
      {label}
    </span>
  );
}

export function Markdown({ children }: { children: string }) {
  return (
    <div className="prose-af">
      <ReactMarkdown remarkPlugins={[remarkGfm]}
        components={{ a: ({ node: _n, ...p }) => <a {...p} target="_blank" rel="noreferrer noopener" /> }}>
        {children}
      </ReactMarkdown>
    </div>
  );
}

export function Button({ variant = "ghost", className = "", ...p }:
  React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "ghost" | "outline" }) {
  const base = "inline-flex items-center justify-center gap-1.5 rounded-lg text-sm font-medium transition disabled:opacity-50 disabled:cursor-not-allowed";
  const v = {
    primary: "bg-accent text-accent-fg px-3.5 py-2 hover:opacity-90",
    outline: "border border-line px-3 py-1.5 hover:bg-sunken",
    ghost: "px-2.5 py-1.5 text-muted hover:text-fg hover:bg-sunken",
  }[variant];
  return <button {...p} className={`${base} ${v} ${className}`} />;
}

export function hostOf(url: string): string {
  try { return new URL(url).hostname.replace(/^www\./, ""); } catch { return url; }
}

export const KIND_TITLE: Record<string, string> = {
  finding: "Findings", intent_cluster: "Intent clusters", competitor: "Competitors", economics: "Economics",
  website_issue: "Website issues", opportunity: "Opportunities", risk: "Risks", decision: "Decisions",
  forecast: "Forecasts", experiment: "Experiments", question: "Open questions",
};

export const ENTRY_PATH_TITLE: Record<string, string> = {
  new_niche: "New niche", website: "Website, no campaigns", ads_account: "Existing Ads account",
};
