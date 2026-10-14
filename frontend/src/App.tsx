import { useCallback, useEffect, useRef, useState } from "react";
import { api, chatStream } from "./api";
import Chat from "./components/Chat";
import KnowledgeView from "./components/KnowledgeView";
import { Entrance, Setup } from "./components/Ignition";
import { Steps, TopBar } from "./components/Rail";
import StagePanel from "./components/StagePanel";
import type { Conversation, Health, Item, Mode, Project, Stage, Turn } from "./types";

const store = {
  get: (k: string) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k: string, v: string) => { try { localStorage.setItem(k, v); } catch { /* storage unavailable */ } },
};

export default function App() {
  const [stages, setStages] = useState<Stage[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [project, setProject] = useState<Project | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [stage, setStage] = useState(3);
  const [view, setView] = useState<"chat" | "knowledge">("chat");
  const [creating, setCreating] = useState(false);
  // The entrance shows once per browser tab session; Enter goes on to the app (or to setup if empty).
  const [entered, setEntered] = useState(() => { try { return sessionStorage.getItem("allfix.entered") === "1"; } catch { return false; } });
  const enter = () => { try { sessionStorage.setItem("allfix.entered", "1"); } catch { /* storage unavailable */ } setEntered(true); };
  const [busy, setBusy] = useState(false);
  const [draft, setDraft] = useState("");
  const [health, setHealth] = useState<Health | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const refreshProject = useCallback(async (id: string) => {
    const p = await api.project(id);
    setProject(p);
    setProjects((list) => list.map((x) => (x.id === p.id ? { ...x, ...p } : x)));
    return p;
  }, []);

  const openProject = useCallback(async (id: string) => {
    store.set("allfix.project", id);
    const [p, convs] = await Promise.all([api.project(id), api.conversations(id)]);
    setProject(p);
    setConversations(convs);
    const c = convs[0] ?? null;
    setConversation(c);
    setTurns(c ? await api.messages(c.id) : []);
  }, []);

  useEffect(() => {
    (async () => {
      try {
        const [h, st, ps] = await Promise.all([api.health(), api.stages(), api.projects()]);
        setHealth(h);
        setStages(st);
        setProjects(ps);
        if (ps.length === 0) { setCreating(true); return; }
        const last = store.get("allfix.project");
        await openProject(ps.find((p) => p.id === last)?.id ?? ps[0].id);
      } catch (e) {
        setLoadError(String(e));
      }
    })();
  }, [openProject]);

  useEffect(() => {
    if (!project) return;
    if (stage === 1 || stage === 7) { setItems([]); return; }
    api.items(project.id, stage).then(setItems).catch(() => setItems([]));
  }, [project?.id, project?.updated_at, stage]);

  const createProject = async (body: Partial<Project>) => {
    const p = await api.createProject(body);
    setProjects((l) => [p, ...l]);
    setCreating(false);
    setStage(p.entry_path === "ads_account" ? 1 : 3);
    await openProject(p.id);
  };

  const newConversation = async () => {
    if (!project) return;
    const c = await api.createConversation(project.id);
    setConversations((l) => [c, ...l]);
    setConversation(c);
    setTurns([]);
  };

  const selectConversation = async (id: string) => {
    const c = conversations.find((x) => x.id === id) ?? null;
    setConversation(c);
    setTurns(c ? await api.messages(c.id) : []);
  };

  const patchLast = (fn: (t: Turn) => Turn) =>
    setTurns((ts) => (ts.length ? [...ts.slice(0, -1), fn(ts[ts.length - 1])] : ts));

  const send = async (text: string, mode: Mode) => {
    if (!project) return;
    let conv = conversation;
    if (!conv) {
      conv = await api.createConversation(project.id);
      setConversations((l) => [conv!, ...l]);
      setConversation(conv);
    }
    setDraft("");
    setBusy(true);
    setTurns((ts) => [...ts, { role: "user", text }, { role: "assistant", text: "", activity: [], streaming: true, mode }]);
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    let afterTool = false;
    try {
      for await (const ev of chatStream(conv.id, text, mode, ctrl.signal)) {
        switch (ev.type) {
          case "turn_start":
            patchLast((t) => ({ ...t, model: ev.model, mode: ev.mode }));
            break;
          case "text": {
            const sep = afterTool; // read now: the updater below runs later, during render
            afterTool = false;
            patchLast((t) => {
              const base = t.text + (sep && t.text ? "\n\n" : "");
              return { ...t, text: base + ev.text, segStart: sep || t.segStart === undefined ? base.length : t.segStart };
            });
            break;
          }
          case "thinking":
            patchLast((t) => ({ ...t, thinking: (t.thinking ?? "") + ev.text }));
            break;
          case "tool_start":
            afterTool = true;
            patchLast((t0) => { const t = demoteNarration(t0); return { ...t, activity: [...(t.activity ?? []).filter((a) => a.id !== ev.id), { id: ev.id, name: ev.name, summary: ev.summary, done: false }] }; });
            break;
          case "tool_end":
            afterTool = true;
            patchLast((t) => ({
              ...t,
              activity: (t.activity ?? []).some((a) => a.id === ev.id)
                ? (t.activity ?? []).map((a) => (a.id === ev.id ? { ...a, done: true, ok: ev.ok, summary: ev.ok ? a.summary : ev.summary } : a))
                : [...(t.activity ?? []), { id: ev.id, name: ev.name, summary: ev.summary, done: true, ok: ev.ok }],
            }));
            break;
          case "item_saved":
            setProject((p) => (p ? { ...p, updated_at: new Date().toISOString() } : p));
            break;
          case "sources":
            patchLast((t) => ({ ...t, sources: ev.sources }));
            break;
          case "error":
            patchLast((t) => ({ ...t, error: ev.message }));
            break;
        }
      }
    } catch (e) {
      if ((e as Error).name !== "AbortError") patchLast((t) => ({ ...t, error: String(e) }));
      else patchLast((t) => ({ ...t, error: "Stopped. Work already done in this turn is saved." }));
    } finally {
      patchLast((t) => ({ ...t, streaming: false, activity: (t.activity ?? []).map((a) => ({ ...a, done: true })) }));
      setBusy(false);
      abortRef.current = null;
      const convs = await api.conversations(project.id).catch(() => null);
      if (convs) { setConversations(convs); setConversation(convs.find((c) => c.id === conv!.id) ?? conv); }
      await refreshProject(project.id).catch(() => undefined);
      api.health().then(setHealth).catch(() => undefined);
    }
  };

  const quote = (item: Item) => {
    setView("chat");
    setDraft((d) => `${d ? d + "\n\n" : ""}About "${item.title}" (item ${item.id}): `);
  };

  const setStatus = async (item: Item, status: string) => {
    await api.updateItem(item.id, { status });
    if (project) await refreshProject(project.id);
  };

  if (loadError) {
    return (
      <div className="frame grid h-full place-items-center p-8 text-center text-fg">
        <div>
          <div className="text-lg font-semibold">AllFix could not reach its server</div>
          <div className="mt-1 text-sm text-muted">{loadError}</div>
          <div className="mt-1 text-sm text-muted">Check that the backend is running and the database is up.</div>
        </div>
      </div>
    );
  }

  if (!entered) return <Entrance onEnter={enter} />;
  if (creating) return <Setup onCreate={createProject} onCancel={() => setCreating(false)} canCancel={projects.length > 0} />;

  return (
    <>
      <div className="frame flex h-full flex-col gap-3 bg-bg p-3 text-fg max-md:h-auto max-md:min-h-full">
        <TopBar projects={projects} project={project} view={view} health={health}
          onSelectProject={(id) => { setView("chat"); openProject(id); }}
          onNewProject={() => setCreating(true)}
          onKnowledge={() => setView("knowledge")} />
        <div className="flex min-h-0 flex-1 gap-3 max-md:flex-col">
          <Steps project={project} stages={stages} stage={stage} view={view}
            onSelectStage={(n) => { setView("chat"); setStage(n); }} />
          {view === "knowledge" ? <div className="sheet flex min-w-0 flex-1 flex-col"><KnowledgeView /></div> : project ? (
            <>
              <Chat project={project} conversations={conversations} conversation={conversation} turns={turns} busy={busy}
                draft={draft} setDraft={setDraft} onSend={send} onStop={() => abortRef.current?.abort()}
                onNewConversation={newConversation} onSelectConversation={selectConversation} />
              <StagePanel project={project} stage={stages.find((s) => s.n === stage)} stages={stages} items={items}
                onQuote={quote} onStatus={setStatus} onSelectStage={setStage}
                onAsk={(text) => { setView("chat"); setDraft(text); }} />
            </>
          ) : <div className="flex-1" />}
        </div>
      </div>
    </>
  );
}

/** A short passage written just before a tool call ("Now saving the plan...") is progress, not the
 * answer: move it into the activity list so the answer starts with the recommendation. */
const NOTE_MAX = 400; // same limit as render_messages in api/routes.py
function demoteNarration(t: Turn): Turn {
  const start = t.segStart ?? 0;
  const seg = t.text.slice(start).trim();
  if (!seg || seg.length > NOTE_MAX) return t;
  const text = t.text.slice(0, start).trimEnd();
  return { ...t, text, segStart: text.length, activity: [...(t.activity ?? []), { id: `note-${(t.activity ?? []).length}`, name: "note", summary: seg, done: true, ok: true }] };
}
