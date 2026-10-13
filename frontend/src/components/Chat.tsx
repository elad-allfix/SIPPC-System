import { useEffect, useRef, useState } from "react";
import type { Activity, Conversation, Mode, Project, Turn } from "../types";
import { Button, Markdown, hostOf } from "./ui";

const TOOL_VERB: Record<string, string> = {
  web_search: "Searching the web", web_fetch: "Reading", search_knowledge: "Searching knowledge",
  read_knowledge: "Reading knowledge", get_project: "Checking the project", update_project: "Updating the project",
  save_item: "Saving", update_item: "Updating", calculate_economics: "Calculating economics",
  record_lesson: "Recording a lesson", WebSearch: "Searching the web", WebFetch: "Reading",
};

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

function AssistantTurn({ t }: { t: Turn }) {
  const [showThinking, setShowThinking] = useState(false);
  const acts = t.activity ?? [];
  return (
    <div className="space-y-3">
      {(acts.length > 0 || t.thinking) && (
        <div className="space-y-1 rounded-lg border border-line/70 bg-sunken/50 px-3 py-2">
          {t.thinking && (
            <button onClick={() => setShowThinking((s) => !s)} className="text-[13px] text-faint hover:text-muted">
              {showThinking ? "Hide reasoning summary" : "Show reasoning summary"}
            </button>
          )}
          {showThinking && t.thinking && <div className="whitespace-pre-wrap pb-1 text-[13px] text-muted">{t.thinking}</div>}
          {acts.slice(-60).map((a) => <ActivityLine key={a.id} a={a} />)}
          {acts.length > 60 && <div className="text-xs text-faint">{acts.length - 60} earlier steps not shown</div>}
        </div>
      )}
      {t.text ? <Markdown>{t.text}</Markdown> : t.streaming && !t.error ? <div className="text-sm text-faint">Working…</div> : null}
      {t.error && <div className="rounded-lg border border-danger/30 bg-danger/5 px-3 py-2 text-sm text-danger">{t.error}</div>}
      {t.sources && t.sources.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {t.sources.slice(0, 30).map((s) => (
            <a key={s.url} href={s.url} target="_blank" rel="noreferrer noopener" title={s.title ?? s.url}
              className="max-w-56 truncate rounded-full border border-line px-2.5 py-0.5 text-xs text-muted hover:border-accent hover:text-fg">
              {hostOf(s.url)}
            </a>
          ))}
        </div>
      )}
      {t.model && !t.streaming && <div className="text-[11px] text-faint">{t.mode === "deep" ? "Deep" : "Standard"} · {t.model}</div>}
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

  const send = () => {
    const text = p.draft.trim();
    if (!text || p.busy) return;
    p.onSend(text, mode);
  };

  return (
    <section className="flex h-full min-w-0 flex-1 flex-col">
      <header className="flex items-center justify-between border-b border-line px-6 py-3">
        <div className="relative min-w-0">
          <button onClick={() => setConvOpen((o) => !o)} className="flex min-w-0 items-center gap-1.5 text-sm font-medium">
            <span className="truncate">{p.conversation?.title ?? "New conversation"}</span>
            <svg className="h-4 w-4 shrink-0 text-faint" viewBox="0 0 20 20" fill="currentColor"><path d="M5.23 7.21a.75.75 0 011.06.02L10 11.17l3.71-3.94a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" /></svg>
          </button>
          {convOpen && (
            <div className="absolute z-20 mt-2 max-h-80 w-80 overflow-auto rounded-lg border border-line bg-panel p-1 shadow-lg scroll-thin">
              {p.conversations.map((c) => (
                <button key={c.id} onClick={() => { setConvOpen(false); p.onSelectConversation(c.id); }}
                  className={`block w-full truncate rounded-md px-2.5 py-1.5 text-left text-sm hover:bg-sunken ${c.id === p.conversation?.id ? "text-accent" : ""}`}>
                  {c.title}
                </button>
              ))}
              {p.conversations.length === 0 && <div className="px-2.5 py-1.5 text-sm text-faint">No conversations yet</div>}
            </div>
          )}
        </div>
        <Button variant="outline" onClick={p.onNewConversation} disabled={p.busy}>New conversation</Button>
      </header>

      <div className="flex-1 overflow-auto scroll-thin">
        <div className="mx-auto max-w-3xl space-y-8 px-6 py-8">
          {p.turns.length === 0 && (
            <div className="pt-10">
              <h1 className="text-xl font-semibold tracking-tight">{p.project.name}</h1>
              <p className="mt-1 text-sm text-muted">
                {p.project.objective || "No objective recorded yet."} Ask anything, or start with one of these.
              </p>
              <div className="mt-6 grid gap-2">
                {(STARTERS[p.project.entry_path] ?? STARTERS.new_niche).map((s) => (
                  <button key={s} onClick={() => p.setDraft(s)}
                    className="rounded-xl border border-line bg-panel px-4 py-3 text-left text-sm hover:border-accent">
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}
          {p.turns.map((t, i) =>
            t.role === "user" ? (
              <div key={i} className="flex justify-end">
                <div className="max-w-[85%] whitespace-pre-wrap rounded-2xl bg-sunken px-4 py-2.5 text-[15px]">{t.text}</div>
              </div>
            ) : <AssistantTurn key={i} t={t} />,
          )}
          <div ref={endRef} />
        </div>
      </div>

      <div className="border-t border-line px-6 py-4">
        <div className="mx-auto max-w-3xl rounded-2xl border border-line bg-panel p-2 focus-within:border-accent">
          <textarea ref={boxRef} value={p.draft} rows={1} data-testid="chat-input"
            onChange={(e) => p.setDraft(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
            placeholder="Ask the strategist…"
            className="block max-h-60 w-full resize-none bg-transparent px-2 py-1.5 text-[15px] outline-none placeholder:text-faint" />
          <div className="flex items-center justify-between pt-1">
            <div className="flex rounded-lg bg-sunken p-0.5 text-xs" role="radiogroup" aria-label="Mode">
              {(["standard", "deep"] as Mode[]).map((m) => (
                <button key={m} role="radio" aria-checked={mode === m} onClick={() => setMode(m)}
                  title={m === "deep" ? "Deeper reasoning for hard strategic questions; slower" : "Default"}
                  className={`rounded-md px-2.5 py-1 capitalize ${mode === m ? "bg-panel font-medium shadow-sm" : "text-muted"}`}>
                  {m}
                </button>
              ))}
            </div>
            {p.busy ? <Button variant="outline" onClick={p.onStop}>Stop</Button>
              : <Button variant="primary" onClick={send} disabled={!p.draft.trim()} data-testid="send">Send</Button>}
          </div>
        </div>
      </div>
    </section>
  );
}
