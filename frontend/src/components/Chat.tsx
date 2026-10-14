import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { Activity, Conversation, FileRef, Mode, Project, Turn } from "../types";
import { Button, Markdown, hostOf } from "./ui";

const TOOL_VERB: Record<string, string> = {
  web_search: "Searching the web", web_fetch: "Reading", search_knowledge: "Searching knowledge",
  read_knowledge: "Reading knowledge", get_project: "Checking the project", update_project: "Updating the project",
  save_item: "Saving", update_item: "Updating", calculate_economics: "Calculating economics",
  record_lesson: "Recording a lesson", read_file: "Reading a file", WebSearch: "Searching the web", WebFetch: "Reading",
};

const ACCEPT = ".csv,.tsv,.txt,.png,.jpg,.jpeg,.webp,.gif";
const ACCOUNT_CHECK = "Account check: read every attached report. First say what each file covers (report type, " +
  "date range, its own totals) and whether conversion tracking can be trusted. Then give one verdict line, " +
  "the 3 numbers that matter most, and the top 5 actions in order. Mark each number as observed from a file or estimated.";
// The strategist reads attachments by id; the line is shown as a chip, not as text.
const ATTACHED = /^\[Attached: (.+) \(file ([0-9a-f-]{36})\)\]$/;

export function attachedLine(f: FileRef) {
  return `[Attached: ${f.name} (file ${f.id})]`;
}

function UserTurn({ text }: { text: string }) {
  const lines = text.split("\n");
  const files = lines.map((l) => ATTACHED.exec(l.trim())).filter(Boolean) as RegExpExecArray[];
  const body = lines.filter((l) => !ATTACHED.test(l.trim())).join("\n").trim();
  return (
    <div className="flex flex-col items-end gap-1.5">
      {body && <div className="max-w-[80%] whitespace-pre-wrap rounded-[22px] rounded-br-md bg-sunken px-4 py-3 text-[15px]">{body}</div>}
      {files.length > 0 && (
        <div className="flex max-w-[85%] flex-wrap justify-end gap-1.5">
          {files.map((m) => <span key={m[2]} className="rounded-full border border-line px-2.5 py-0.5 text-xs text-muted">{m[1]}</span>)}
        </div>
      )}
    </div>
  );
}

const STARTERS: Record<string, string[]> = {
  new_niche: [
    "Research this niche from scratch: demand, intent, competitors, economics and where to start.",
    "What do I need to tell you about the business before you can judge whether Google Ads can work?",
  ],
  website: [
    "Research the market, then review my website against what searchers in this niche need.",
    "Which searches should this website be able to win, and what stops it today?",
  ],
  ads_account: [
    "Check the account from the reports I attached: one verdict, the 3 numbers that matter, then the top 5 actions.",
    "Before connecting the account, research the market so we know what good looks like.",
    "What will you check first once the account is connected, and why?",
  ],
};

interface Props {
  project: Project;
  conversations: Conversation[];
  conversation: Conversation | null;
  turns: Turn[];
  busy: boolean;
  draft: string;
  setDraft: (s: string) => void;
  onSend: (text: string, mode: Mode) => void;
  onStop: () => void;
  onNewConversation: () => void;
  onSelectConversation: (id: string) => void;
}

function ActivityLine({ a }: { a: Activity }) {
  if (a.name === "note") return <div className="text-[13px] italic text-muted">{a.summary}</div>;
  const state = a.ok === false ? "text-danger" : a.done === false ? "text-muted" : "text-faint";
  return (
    <div className={`flex items-center gap-2 text-[13px] ${state}`}>
      {a.done === false ? <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-accent" />
        : <span className={`h-1.5 w-1.5 rounded-full ${a.ok === false ? "bg-danger" : "bg-line"}`} />}
      <span className="truncate">
        {TOOL_VERB[a.name] ?? a.name}{a.summary ? <span className="text-muted">: {a.summary}</span> : null}
        {a.ok === false ? " (failed)" : ""}
      </span>
    </div>
  );
}

/** The answer comes first. Steps, reasoning and sources fold behind one small "Details" link;
 * while the strategist works, only its latest few steps show. */
function AssistantTurn({ t }: { t: Turn }) {
  const [open, setOpen] = useState(false);
  const acts = t.activity ?? [];
  const sources = t.sources ?? [];
  const hasDetails = acts.length > 0 || !!t.thinking || sources.length > 0;
  return (
    <div className="space-y-3">
      {t.streaming && acts.length > 0 && !open && (
        <div className="space-y-1">{acts.slice(-3).map((a) => <ActivityLine key={a.id} a={a} />)}</div>
      )}
      {t.text ? <Markdown>{t.text}</Markdown> : t.streaming && !t.error ? (
        <div className="flex items-center gap-2 text-sm text-faint"><span className="h-2 w-2 animate-pulse rounded-full bg-accent" />Working…</div>
      ) : null}
      {t.error && <div className="rounded-xl border border-danger/30 bg-danger/5 px-3 py-2 text-sm text-danger">{t.error}</div>}
      {hasDetails && !t.streaming && (
        <button onClick={() => setOpen((o) => !o)} className="text-xs text-faint hover:text-fg">
          {open ? "Hide details" : "Details"}
        </button>
      )}
      {open && (
        <div className="space-y-3 rounded-2xl bg-sunken px-4 py-3">
          {t.thinking && <div className="whitespace-pre-wrap text-[13px] text-muted">{t.thinking}</div>}
          {acts.length > 0 && <div className="space-y-1">
            {acts.slice(-60).map((a) => <ActivityLine key={a.id} a={a} />)}
            {acts.length > 60 && <div className="text-xs text-faint">{acts.length - 60} earlier steps not shown</div>}
          </div>}
          {sources.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {sources.slice(0, 30).map((s) => (
                <a key={s.url} href={s.url} target="_blank" rel="noreferrer noopener" title={s.title ?? s.url}
                  className="max-w-56 truncate rounded-full border border-line bg-panel px-2.5 py-0.5 text-xs text-muted hover:border-accent hover:text-fg">
                  {hostOf(s.url)}
                </a>
              ))}
            </div>
          )}
          {t.model && <div className="text-[11px] text-faint">{t.mode === "deep" ? "Deep" : "Fast"} · {t.model}</div>}
        </div>
      )}
    </div>
  );
}

export default function Chat(p: Props) {
  const [mode, setMode] = useState<Mode>("standard");
  const [convOpen, setConvOpen] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);
  const boxRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => { endRef.current?.scrollIntoView({ block: "end" }); }, [p.turns]);
  useEffect(() => {
    const el = boxRef.current;
    if (el) { el.style.height = "auto"; el.style.height = Math.min(el.scrollHeight, 240) + "px"; }
  }, [p.draft]);

  const [attached, setAttached] = useState<FileRef[]>([]);
  const [uploading, setUploading] = useState(0);
  const [uploadError, setUploadError] = useState("");
  const [uploadNotes, setUploadNotes] = useState<string[]>([]);
  const fileRef = useRef<HTMLInputElement>(null);

  const checkRef = useRef<HTMLInputElement>(null);

  const upload = async (files: File[]) => {
    setUploadError("");
    setUploadNotes([]);
    const done: FileRef[] = [];
    for (const f of files) {
      setUploading((n) => n + 1);
      try {
        const ref = await api.uploadFile(p.project.id, f);
        done.push(ref);
        if (ref.note) setUploadNotes((n) => [...n, `${f.name}: ${ref.note!.replace(/^AllFix reduced this file on arrival: /, "")}`]);
        setAttached((a) => [...a, ref]);
      } catch (e) {
        setUploadError(`${f.name}: ${(e as Error).message}`);
      } finally {
        setUploading((n) => n - 1);
      }
    }
    return done;
  };

  // Account check: pick the account's report exports, upload them, and ask for one verdict,
  // 3 numbers and the top 5 actions.
  const accountCheck = async (files: File[]) => {
    const done = await upload(files);
    const all = [...attached, ...done];
    if (all.length === 0 || p.busy) return;
    p.onSend([ACCOUNT_CHECK, ...all.map(attachedLine)].join("\n"), "deep"); // the account verdict gets the deeper model
    setAttached([]);
  };

  const send = () => {
    const text = p.draft.trim();
    if ((!text && attached.length === 0) || p.busy || uploading > 0) return;
    const lines = attached.map(attachedLine);
    p.onSend([text || "I attached a file.", ...lines].join("\n"), mode);
    setAttached([]);
    setUploadError("");
    setUploadNotes([]);
  };

  return (
    <section className="sheet flex min-w-0 flex-1 flex-col max-md:min-h-[80vh]">
      <header className="flex items-center justify-between gap-3 px-7 pb-2 pt-5">
        <div className="relative min-w-0">
          <button onClick={() => setConvOpen((o) => !o)} className="flex min-w-0 items-center gap-1.5 text-lg font-bold tracking-tight">
            <span className="truncate">{p.conversation?.title ?? "New conversation"}</span>
            <svg className="h-4 w-4 shrink-0 text-faint" viewBox="0 0 20 20" fill="currentColor"><path d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" /></svg>
          </button>
          {convOpen && (
            <div className="absolute z-20 mt-2 max-h-80 w-80 overflow-auto rounded-2xl border border-line bg-panel p-1.5 shadow-xl scroll-thin">
              {p.conversations.map((c) => (
                <button key={c.id} onClick={() => { setConvOpen(false); p.onSelectConversation(c.id); }}
                  className={`block w-full truncate rounded-xl px-3 py-2 text-left text-sm hover:bg-sunken ${c.id === p.conversation?.id ? "font-semibold text-accent-ink" : ""}`}>
                  {c.title}
                </button>
              ))}
              {p.conversations.length === 0 && <div className="px-2.5 py-1.5 text-sm text-faint">No conversations yet</div>}
            </div>
          )}
        </div>
        <Button variant="primary" onClick={p.onNewConversation} disabled={p.busy}>New question</Button>
      </header>

      <div className="flex-1 overflow-auto scroll-thin">
        <div className="mx-auto max-w-3xl space-y-8 px-7 py-6">
          {p.turns.length === 0 && (
            <div className="pt-8">
              <h1 className="text-3xl font-bold tracking-[-0.035em]">{p.project.name}</h1>
              {p.project.objective && <p className="mt-2 text-muted">{p.project.objective}</p>}
              <div className="mt-6 grid gap-2">
                {(STARTERS[p.project.entry_path] ?? STARTERS.new_niche).map((s) => (
                  <button key={s} onClick={() => p.setDraft(s)}
                    className="rounded-2xl bg-sunken px-4 py-3 text-left text-sm hover:ring-1 hover:ring-accent">
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}
          {p.turns.map((t, i) =>
            t.role === "user" ? (
              <UserTurn key={i} text={t.text} />
            ) : <AssistantTurn key={i} t={t} />,
          )}
          <div ref={endRef} />
        </div>
      </div>

      <div className="px-6 pb-6 pt-2">
        <div className="mx-auto max-w-3xl rounded-[22px] border border-line bg-panel p-2.5 shadow-[0_12px_30px_-18px_rgba(22,23,26,.35)] focus-within:border-accent">
          {(attached.length > 0 || uploading > 0 || uploadError || uploadNotes.length > 0) && (
            <div className="flex flex-wrap items-center gap-1.5 px-2 pb-1.5">
              {attached.map((f) => (
                <span key={f.id} className="flex items-center gap-1 rounded-full border border-line px-2.5 py-0.5 text-xs text-muted">
                  {f.name}
                  <button aria-label={`Remove ${f.name}`} onClick={() => setAttached((a) => a.filter((x) => x.id !== f.id))}
                    className="text-faint hover:text-fg">×</button>
                </span>
              ))}
              {uploading > 0 && <span className="text-xs text-faint">Uploading… big exports take a minute</span>}
              {uploadError && <span className="text-xs text-danger">{uploadError}</span>}
              {uploadNotes.map((n, i) => <span key={i} className="w-full text-xs text-faint">{n}</span>)}
            </div>
          )}
          <textarea ref={boxRef} value={p.draft} rows={1} data-testid="chat-input"
            onChange={(e) => p.setDraft(e.target.value)}
            onPaste={(e) => {
              const files = Array.from(e.clipboardData.files);
              if (files.length) { e.preventDefault(); upload(files.map((f, i) =>
                f.name && f.name !== "image.png" ? f : new File([f], `screenshot-${Date.now()}-${i}.png`, { type: f.type }))); }
            }}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            placeholder="Ask anything"
            className="block max-h-60 w-full resize-none bg-transparent px-2 py-1.5 text-[15px] outline-none placeholder:text-faint" />
          <div className="flex items-center justify-between pt-1">
            <div className="flex items-center gap-2">
            <input ref={fileRef} type="file" multiple accept={ACCEPT} className="hidden" data-testid="file-input"
              onChange={(e) => { upload(Array.from(e.target.files ?? [])); e.target.value = ""; }} />
            <button onClick={() => fileRef.current?.click()} aria-label="Attach files" data-testid="attach"
              title="Attach a CSV/TSV report export or a screenshot (you can also paste a screenshot)"
              className="rounded-md p-1.5 text-muted hover:bg-sunken hover:text-fg">
              <svg className="h-4 w-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.6"><path d="M15.5 9.5l-5.8 5.8a3.5 3.5 0 01-5-5l6.4-6.4a2.3 2.3 0 013.3 3.3l-6.3 6.3a1.2 1.2 0 01-1.7-1.7L12 6.2" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </button>
            <input ref={checkRef} type="file" multiple accept=".csv,.tsv,.txt" className="hidden" data-testid="check-input"
              onChange={(e) => { accountCheck(Array.from(e.target.files ?? [])); e.target.value = ""; }} />
            <button onClick={() => checkRef.current?.click()} disabled={p.busy || uploading > 0} data-testid="account-check"
              title="Upload Google Ads report exports (campaigns, search terms, keywords, ads, conversions) and get one verdict, 3 numbers and the top 5 actions. Always runs in Deep mode."
              className="rounded-full border border-line px-3 py-1 text-xs text-muted hover:bg-sunken hover:text-fg disabled:opacity-40">
              Account check
            </button>
            <div className="flex rounded-full bg-sunken p-0.5 text-xs" role="radiogroup" aria-label="Mode">
              {(["standard", "deep"] as Mode[]).map((m) => (
                <button key={m} role="radio" aria-checked={mode === m} onClick={() => setMode(m)}
                  title={m === "deep" ? "Deeper reasoning for hard strategic questions; slower" : "Quick answers"}
                  className={`rounded-full px-3 py-1 ${mode === m ? "bg-panel font-semibold shadow-sm" : "text-faint"}`}>
                  {m === "deep" ? "Deep" : "Fast"}
                </button>
              ))}
            </div>
            </div>
            {p.busy ? <Button variant="outline" onClick={p.onStop}>Stop</Button>
              : <button onClick={send} disabled={(!p.draft.trim() && attached.length === 0) || uploading > 0} data-testid="send"
                  aria-label="Send" className="grid h-10 w-10 place-items-center rounded-full bg-ink text-lg font-bold text-ink-fg transition hover:opacity-90 disabled:opacity-30">↑</button>}
          </div>
        </div>
      </div>
    </section>
  );
}
