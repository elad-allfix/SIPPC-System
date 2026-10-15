import type { Connectivity, FileRef, ConnectionProfile, Conversation, Health, Item, Lesson, Project, ProjectCard, Stage, Turn, Mode, Run, Verification } from "./types";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`/api${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const j = await res.json();
      detail = typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail);
    } catch { /* not json */ }
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.status === 204 ? (undefined as T) : res.json();
}

export const api = {
  health: () => req<Health>("/health"),
  stages: () => req<Stage[]>("/stages"),
  projects: () => req<Project[]>("/projects"),
  overview: () => req<ProjectCard[]>("/overview"),
  needs: (id: string) => req<ProjectCard>(`/projects/${id}/needs`),
  lessons: (id: string) => req<Lesson[]>(`/projects/${id}/lessons`),
  project: (id: string) => req<Project>(`/projects/${id}`),
  createProject: (body: Partial<Project>) => req<Project>("/projects", { method: "POST", body: JSON.stringify(body) }),
  updateProject: (id: string, body: Partial<Project>) =>
    req<Project>(`/projects/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  deleteProject: (id: string) => req<void>(`/projects/${id}`, { method: "DELETE" }),
  items: (projectId: string, stage?: number) =>
    req<Item[]>(`/projects/${projectId}/items${stage ? `?stage=${stage}` : ""}`),
  updateItem: (id: string, body: Partial<Item> & { append_note?: string }) =>
    req<Item>(`/items/${id}`, { method: "PATCH", body: JSON.stringify(body) }),
  scoreItem: (id: string, body: { actual: string; verdict: string; evidence?: string }) =>
    req<Item>(`/items/${id}/outcome`, { method: "POST", body: JSON.stringify(body) }),
  conversations: (projectId: string) => req<Conversation[]>(`/projects/${projectId}/conversations`),
  createConversation: (projectId: string, title = "New conversation") =>
    req<Conversation>(`/projects/${projectId}/conversations`, { method: "POST", body: JSON.stringify({ title }) }),
  messages: (conversationId: string) => req<Turn[]>(`/conversations/${conversationId}/messages`),
  connectivity: (projectId: string) => req<Connectivity>(`/projects/${projectId}/connectivity`),
  saveConnectivity: (projectId: string, body: Partial<ConnectionProfile>) =>
    req<ConnectionProfile>(`/projects/${projectId}/connectivity`, { method: "PUT", body: JSON.stringify(body) }),
  verifyRoute: (projectId: string) => req<Verification>(`/projects/${projectId}/connectivity/verify`, { method: "POST" }),
  importAds: (projectId: string, days = 90) => req<any>(`/projects/${projectId}/ads/import?days=${days}`, { method: "POST" }),
  runs: (projectId: string) => req<Run[]>(`/projects/${projectId}/runs`),
  accountCheck: (projectId: string, force = false) =>
    req<any>(`/projects/${projectId}/checks/account${force ? "?force=true" : ""}`, { method: "POST" }),
  files: (projectId: string) => req<FileRef[]>(`/projects/${projectId}/files`),
  uploadFile: async (projectId: string, file: File): Promise<FileRef> => {
    const res = await fetch(`/api/projects/${projectId}/files?name=${encodeURIComponent(file.name)}`, {
      method: "POST", body: file, headers: { "Content-Type": "application/octet-stream" },
    });
    if (!res.ok) {
      let detail = res.statusText;
      try { const j = await res.json(); if (typeof j.detail === "string") detail = j.detail; } catch { /* not json */ }
      throw new Error(detail);
    }
    return res.json();
  },
  knowledgeSearch: (q: string) => req<{ entries: any[]; documents: any[] }>(`/knowledge/search?q=${encodeURIComponent(q)}&limit=20`),
  knowledgeDocuments: () => req<any[]>("/knowledge/documents"),
  knowledgeRead: (id: string) => req<any>(`/knowledge/${encodeURIComponent(id)}`),
};

export type ChatEvent = { type: string; [k: string]: any };

/** POST a chat message and yield server-sent events as they arrive. */
export async function* chatStream(conversationId: string, message: string, mode: Mode, signal?: AbortSignal): AsyncGenerator<ChatEvent> {
  const res = await fetch(`/api/conversations/${conversationId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, mode }),
    signal,
  });
  if (!res.ok || !res.body) {
    yield { type: "error", message: `Request failed (${res.status})` };
    return;
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx: number;
    while ((idx = buf.indexOf("\n\n")) >= 0) {
      const chunk = buf.slice(0, idx);
      buf = buf.slice(idx + 2);
      const data = chunk.split("\n").filter((l) => l.startsWith("data:")).map((l) => l.slice(5).trimStart()).join("\n");
      if (!data) continue;
      try {
        yield JSON.parse(data);
      } catch { /* ignore malformed chunk */ }
    }
  }
}
