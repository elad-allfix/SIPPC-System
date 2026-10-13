import { useEffect, useState } from "react";
import { api } from "../api";
import { Markdown } from "./ui";

export default function KnowledgeView() {
  const [q, setQ] = useState("");
  const [res, setRes] = useState<{ entries: any[]; documents: any[] } | null>(null);
  const [docs, setDocs] = useState<any[]>([]);
  const [open, setOpen] = useState<any | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => { api.knowledgeDocuments().then(setDocs).catch(() => setDocs([])); }, []);

  const search = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!q.trim()) return;
    setErr(null);
    try { setRes(await api.knowledgeSearch(q)); } catch (x) { setErr(String(x)); }
  };
  const read = async (id: string) => {
    try { setOpen(await api.knowledgeRead(id)); } catch (x) { setErr(String(x)); }
  };

  return (
    <section className="flex h-full min-w-0 flex-1">
      <div className="flex w-[26rem] shrink-0 flex-col border-r border-line">
        <form onSubmit={search} className="border-b border-line p-4">
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search the knowledge base, or an id like PLT-BID-007"
            className="w-full rounded-lg border border-line bg-panel px-3 py-2 text-sm outline-none focus:border-accent" data-testid="kb-search" />
        </form>
        <div className="flex-1 space-y-1 overflow-auto p-2 scroll-thin">
          {err && <div className="p-2 text-sm text-danger">{err}</div>}
          {!res && (
            <>
              <div className="px-2 py-1 text-[11px] font-medium uppercase tracking-wider text-faint">Documents</div>
              {docs.map((d) => (
                <button key={d.slug} onClick={() => read(d.slug)} className="block w-full rounded-lg px-2 py-1.5 text-left text-sm hover:bg-sunken">
                  {d.title}<span className="ml-2 text-xs text-faint">{d.kind}</span>
                </button>
              ))}
            </>
          )}
          {res && res.entries.length === 0 && res.documents.length === 0 && <div className="p-2 text-sm text-muted">No matches.</div>}
          {res?.documents.map((d) => (
            <button key={d.slug} onClick={() => read(d.slug)} className="block w-full rounded-lg px-2 py-1.5 text-left text-sm hover:bg-sunken">
              {d.title}<span className="ml-2 text-xs text-faint">{d.kind}</span>
            </button>
          ))}
          {res?.entries.map((e) => (
            <button key={e.id} onClick={() => read(e.id)} className="block w-full rounded-lg px-2 py-2 text-left hover:bg-sunken">
              <div className="text-xs text-faint">{e.id} · {e.evidence_type} · {e.confidence}</div>
              <div className="text-sm font-medium">{e.title}</div>
              <div className="line-clamp-2 text-xs text-muted">{e.claim}</div>
            </button>
          ))}
        </div>
      </div>
      <div className="flex-1 overflow-auto scroll-thin">
        {open ? (
          <article className="mx-auto max-w-3xl px-8 py-8">
            <div className="text-xs text-faint">{open.id}{open.evidence_type ? ` · ${open.evidence_type}` : ""}{open.confidence ? ` · ${open.confidence}` : ""}</div>
            <h1 className="mb-4 text-lg font-semibold">{open.title}</h1>
            <Markdown>{String(open.body ?? "").replace(/^#{1,4} .*\n+/, "")}</Markdown>
          </article>
        ) : <div className="grid h-full place-items-center text-sm text-faint">This is the same knowledge the strategist searches.</div>}
      </div>
    </section>
  );
}
