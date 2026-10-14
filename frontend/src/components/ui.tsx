import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Label } from "../types";

/** How sure we are, in plain words, strongest first; colours come from the --ev-* tokens. */
export const LABEL_ORDER: Label[] = ["verified", "observed", "estimate", "hypothesis", "assumption", "unknown"];
export const LABEL_NAME: Record<Label, string> = {
  verified: "Checked", observed: "Seen", estimate: "Estimate", hypothesis: "To test", assumption: "Assumed", unknown: "Unknown",
};
export const labelColor = (l: Label) => `var(--ev-${LABEL_NAME[l] ? l : "unknown"})`;

export const LABEL_HELP: Record<Label, string> = {
  verified: "Checked against a primary source",
  observed: "Seen directly (a page, a results page, a tool output)",
  estimate: "A number derived from evidence, with a range",
  assumption: "Taken as given for planning; not checked",
  hypothesis: "A testable idea",
  unknown: "Not known yet",
};

export function LabelDot({ label, className = "" }: { label: Label; className?: string }) {
  return <span title={`${LABEL_NAME[label] ?? label}: ${LABEL_HELP[label] ?? ""}`} aria-label={LABEL_NAME[label] ?? label}
    className={`inline-block h-2.5 w-2.5 shrink-0 rounded-full ${className}`} style={{ background: labelColor(label) }} />;
}

export function LabelBadge({ label }: { label: Label }) {
  return (
    <span title={LABEL_HELP[label]} className="inline-flex items-center gap-1.5 whitespace-nowrap text-[11px] font-medium text-muted">
      <LabelDot label={label} className="!h-2 !w-2" />{LABEL_NAME[label] ?? label}
    </span>
  );
}

/** Thin stacked bar of how many items sit at each evidence level, with a short key. */
export function EvidenceScale({ labels }: { labels: Label[] }) {
  if (labels.length === 0) return null;
  const counts = LABEL_ORDER.map((l) => [l, labels.filter((x) => x === l).length] as const).filter(([, n]) => n > 0);
  return (
    <div className="space-y-2">
      <div className="flex h-2 gap-0.5 overflow-hidden rounded-full" role="img"
        aria-label={counts.map(([l, n]) => `${n} ${LABEL_NAME[l]}`).join(", ")}>
        {counts.map(([l, n]) => <i key={l} className="block h-full" style={{ flex: n, background: labelColor(l) }} />)}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-faint">
        {counts.map(([l, n]) => (
          <span key={l} className="inline-flex items-center gap-1.5"><LabelDot label={l} className="!h-2 !w-2" />{LABEL_NAME[l]} {n}</span>
        ))}
      </div>
    </div>
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
  const base = "inline-flex items-center justify-center gap-1.5 rounded-full text-sm font-medium transition disabled:opacity-50 disabled:cursor-not-allowed";
  const v = {
    primary: "bg-ink text-ink-fg px-4 py-2 font-semibold hover:opacity-90",
    outline: "border border-line bg-panel px-3.5 py-1.5 hover:bg-sunken",
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
