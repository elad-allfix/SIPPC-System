export type Label = "verified" | "observed" | "estimate" | "assumption" | "hypothesis" | "unknown";
export type EntryPath = "new_niche" | "website" | "ads_account";
export type ObjectiveType = "profit" | "leads" | "sales" | "traffic" | "awareness" | "unknown";
export type Mode = "standard" | "deep";

export interface Stage { n: number; key: string; title: string; summary: string }

export interface Fact { key: string; value: string; label: Label; source: string; updated_at: string }

export interface Project {
  id: string;
  name: string;
  entry_path: EntryPath;
  objective: string;
  objective_type: ObjectiveType;
  country: string | null;
  region: string | null;
  language: string | null;
  website_url: string | null;
  notes: string;
  created_at: string;
  updated_at: string;
  item_count?: number;
  facts?: Fact[];
  stage_counts?: Record<string, Record<string, number>>;
}

export interface ProjectCard extends Project {
  file_count: number;
  conversation_count: number;
  last_activity: string | null;
  item_counts: Record<string, number>;
  item_total: number;
  stages_with_items: number[];
  plan: string | null;
  needs: { kind: "do" | "check" | "answer" | "fix" | "risk"; text: string; item_id?: string; stage?: number }[];
}

export interface Source { url?: string; title?: string; note?: string; kb?: string; checked?: string }

export interface Item {
  id: string;
  project_id: string;
  stage: number;
  kind: string;
  title: string;
  body: string;
  data: Record<string, unknown>;
  label: Label;
  confidence: "high" | "medium" | "low" | null;
  sources: Source[];
  status: string;
  superseded_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface Conversation { id: string; project_id: string; title: string; created_at: string; updated_at: string }

export interface Activity { id: string; name: string; summary: string; ok?: boolean; done?: boolean }

export interface Turn {
  role: "user" | "assistant";
  text: string;
  thinking?: string;
  activity?: Activity[];
  sources?: { url: string; title?: string | null }[];
  model?: string | null;
  mode?: string | null;
  error?: string;
  streaming?: boolean;
  segStart?: number; // where the text written since the last tool call begins
}

export interface KbHit {
  id: string;
  title: string;
  area?: string;
  claim?: string;
  evidence_type?: string;
  confidence?: string;
  kind?: string;
}

export interface Health {
  ok: boolean;
  knowledge_entries: number;
  backend: "subscription" | "api";
  models: Record<string, string>;
  subscription?: { api_key_source: string | null; rate_limit: Record<string, any> | null; checked_at: string | null };
}

export interface RouteCheck { name: string; ok: boolean | null; detail: string }

export interface Verification {
  ok: boolean;
  public_ip: string | null;
  country: string | null;
  region: string | null;
  at: string;
  checks: RouteCheck[];
}

export interface ConnectionProfile {
  id: string;
  ads_customer_id: string | null;
  login_customer_id: string | null;
  required_country: string;
  required_region: string | null;
  vpn_profile: string | null;
  dolphin_profile_id: string | null;
  last_verified_at: string | null;
  last_result: Verification | null;
}

export interface AdsSnapshot {
  id: string;
  customer_id: string;
  taken_at: string;
  date_range: string;
  status: "running" | "done" | "failed";
  error: string | null;
  summary: Record<string, any>;
}

export interface Connectivity {
  profile: ConnectionProfile | null;
  ads_configured: boolean;
  ads_api_version: string;
  snapshot: AdsSnapshot | null;
}

export interface RunFinding { check: string; severity: "high" | "medium" | "low"; title: string; detail: string; label: string }

export interface Run {
  id: string;
  kind: string;
  run_date: string;
  status: "running" | "done" | "failed" | "skipped";
  attention: boolean;
  summary: string;
  error: string | null;
  findings: RunFinding[] | null;
  metrics: Record<string, any> | null;
}

export interface FileRef {
  id: string;
  name: string;
  mime: string;
  size_bytes: number;
  created_at: string;
  note?: string; // set when a large export was reduced on arrival
}
