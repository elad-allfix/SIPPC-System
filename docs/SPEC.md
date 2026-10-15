# AllFix: technical specification (v1)

Status: implementation spec, 2026-10-13. This is the build reference. It assumes the agreed product direction (one AI strategist, the seven-stage workflow, Google Ads first) and does not restate it.

## 1. Architecture in one picture

```
Browser (React)                     Your PC or a cloud host
┌──────────────────────┐   HTTP/SSE  ┌──────────────────────────────────────────┐
│ Seven-stage rail      │ ─────────▶ │ FastAPI app (one Python process)          │
│ Strategist chat       │ ◀───────── │  ├─ Strategist loop ─▶ Claude API          │
│ Stage panel           │            │  │    (Opus 5.5; Deep = max thinking)     │
└──────────────────────┘            │  │    server tools: web_search, web_fetch  │
                                     │  │    our tools: knowledge, memory, math   │
                                     │  ├─ Data & Research (fetchers, page audit) │
                                     │  ├─ Marketing Intelligence (KB + economics)│
                                     │  └─ Connectivity guard (Stage 01, Phase 5) │
                                     └───────────────┬──────────────────────────┘
                                                     │ SQL
                                       Postgres (local, or Supabase as plain Postgres)
```

One process and one database. The three capabilities are Python packages inside the same app, not separate services. The seven stages are a way of organising the work in the interface and the data, not seven backends.

## 2. Technology choices

| Concern | Choice | Why |
|---|---|---|
| Backend | Python 3.12+, FastAPI, Uvicorn | Google's official Google Ads API client is Python. It has the best data and analysis libraries, and the official Anthropic SDK. |
| Database | PostgreSQL 16+ through psycopg 3, with plain SQL migrations | Runs on a PC and in the cloud. Supabase is used only as hosted Postgres, so moving off it means a dump and restore. No ORM. |
| Search over knowledge | Postgres full-text search (`tsvector`) | Enough for 375 entries with IDs and labels. Vector search (pgvector) is added only if retrieval tests show a need. |
| AI | Anthropic Python SDK behind a small `ModelClient` interface | A model is a config value. Another provider can be added behind the same interface. |
| Frontend | React + TypeScript + Vite + Tailwind CSS | Mainstream, fast, and builds to static files that FastAPI serves, so there is still one process. |
| Streaming | Server-sent events over a POST response | Simple, and works through proxies. |
| Local run | `scripts/setup.ps1` (Windows) and `scripts/setup.sh` | Creates the Python environment, builds the interface and runs migrations. Postgres comes from a local install or `docker compose`. |

## 3. Repository layout

```
allfix/
  backend/allfix/
    config.py            settings from environment (.env)
    db.py                connection pool + migration runner
    migrations/          001_init.sql, 002_...
    knowledge/           loader (markdown -> kb_entries), search
    intelligence/        economics.py (value per click, break-even), later analyses
    research/            page_audit.py (Phase 4), sources registry
    connect/             Stage 01 guard (Phase 5)
    strategist/          prompt.py, tools.py, loop.py, models.py
    api/                 routes: projects, conversations, items, knowledge, health
    main.py              app factory, static frontend
  backend/tests/
  frontend/              Vite app
  knowledge/             the AllFix knowledge base (markdown, versioned with the code)
  scripts/               setup, run, backup (PowerShell + bash)
  docs/                  SPEC.md (this file), ROADMAP.md
  docker-compose.yml     optional local Postgres
  .env.example
```

## 4. Data model (Postgres)

| Table | Purpose | Key columns |
|---|---|---|
| `projects` | One per business or niche | id, name, entry_path (`new_niche` / `website` / `ads_account`), objective (free text), objective_type (`profit` / `leads` / `sales` / `traffic` / `awareness` / `unknown`), market (country, region, language), website_url, created_at |
| `project_facts` | Business facts with provenance | project_id, key, value, label, source, updated_at. Examples: margin, average order value, close rate, capacity, service area |
| `conversations` | Chat threads inside a project | id, project_id, title, created_at |
| `messages` | Full API message content, append-only | conversation_id, seq, role, content (jsonb, exact API blocks), model, usage (jsonb), created_at |
| `items` | Everything the strategist saves | id, project_id, stage (1–7), kind, title, body (markdown), data (jsonb), label, confidence, sources (jsonb), status, created_at, superseded_by |
| `lessons` | Corrections and lessons across projects | id, project_id (nullable), what_was_wrong, correction, applies_to, kb_entry_ids, created_at |
| `kb_entries` | The knowledge base, indexed | id (e.g. PLT-AUC-009), file, area, title, claim, body, evidence_type, confidence, changed, search (tsvector) |
| `kb_documents` | Playbooks, relationship map, demo | slug, title, body, search |
| `connection_profiles` | Stage 01 (Phase 5) | project_id, ads_customer_id, required_country, required_region, vpn_profile, dolphin_profile_id, last_verified_at, last_result |
| `runs` | Scheduled rounds (Phase 6) | id, project_id, kind, status, started_at, finished_at, summary |

`items.kind` covers every saved object: `finding`, `intent_cluster`, `competitor`, `economics`, `website_issue`, `opportunity`, `risk`, `decision`, `forecast`, `experiment`, `question`. This is one table rather than eleven. The kind decides how the interface shows an item and which stage it belongs to by default. Decisions and forecasts are items with structured `data`; together they form the Decision Journal and the Forecast Ledger.

**Labels** come from one vocabulary everywhere: `verified` (opened source), `observed` (seen directly, for example on a results page), `estimate` (calculated or third-party, basis shown), `assumption` (supplied or chosen, not checked), `hypothesis`, `unknown`.

## 5. The strategist

**Loop.** A manual streaming tool loop on the Claude Messages API:
- It sends the conversation history from `messages` (append-only, so thinking blocks stay valid).
- It runs our tools and appends their results.
- It resumes `pause_turn` for server tools.
- It stops at `end_turn` or after a step cap (default 40 tool calls per turn).
- It streams text, tool activity and summarised thinking to the browser as SSE events.

**Models** (config in `strategist/models.py`):

| Mode | Model | Effort | Use |
|---|---|---|---|
| `standard` | `claude-opus-5-5` | high | Conversation, diagnosis, most research |
| `deep` | `claude-opus-5-5` | max | Full niche research, strategy, hard judgement calls (user toggle). Was Fable 5.1 until 2026-10-15; Elad chose Opus 5.5 at maximum thinking after Fable was refused on his PC |

Every request:
- uses adaptive thinking with summarised display
- adds server-side refusal fallback (`fallbacks: "default"`)
- caches the system prompt and tool list
- turns on server-side compaction for long conversations

Each model is one config line, so the evaluation set can decide later whether a cheaper model handles some routes.

**System prompt** (stable, cached) covers:
- the role and principles: honesty, labels, no invented numbers, challenge assumptions, recommend doing nothing when warranted, practitioner numbers are priors
- the intent-chain method
- how to use the tools
- the label vocabulary

A short **project brief** is added per request after the cache breakpoint:
- the project profile and facts
- counts and titles of saved items per stage
- the latest decisions
- lessons that apply

Full items and knowledge entries are fetched by tools, never preloaded.

**Tools.**

| Tool | Kind | What it does |
|---|---|---|
| `web_search`, `web_fetch` | Anthropic server tools | Current web research: SERP-like results, competitor pages, news, regulations. Results carry citations, which are stored as sources. |
| `search_knowledge` | ours | Full-text search over `kb_entries` and `kb_documents`. Returns ids, titles, claims, evidence types and confidence. |
| `read_knowledge` | ours | Full text of named entries or a playbook. |
| `get_project` | ours | Profile, facts, and saved items filtered by stage or kind. |
| `update_project` | ours | Sets profile fields or facts, each with a label and source. |
| `save_item` | ours | Saves a finding, cluster, competitor, economics result, opportunity, risk, decision, forecast or question, with stage, label, confidence and sources. |
| `update_item` | ours | Changes status or supersedes an item, for example when a hypothesis is confirmed or refuted. |
| `calculate_economics` | ours | Deterministic arithmetic: value per click, break-even CPC and ROAS, and a sensitivity table across ranges of inputs. The model never does this arithmetic in its head. |
| `record_lesson` | ours | Stores a correction so future reasoning sees it. |
| `audit_page` | ours (Phase 4) | Fetches a URL and extracts the facts that matter: headings, CTAs, forms and fields, trust signals, tracking tags, response time, mobile viewport. |
| `ads_query` | ours (Phase 5) | Read-only Google Ads API (GAQL) through the Stage 01 guard. |

## 6. Research sources and their limits

| Source | Available | Gives | Does not give |
|---|---|---|---|
| Claude web search + fetch | Phase 2 | Current pages, competitor sites, news, regulations, reviews, forum language | Search volumes, CPCs, the exact Google results page a given user sees, ad copy in Google's Ads Transparency Center (which needs JavaScript) |
| Our page audit | Phase 4 | Structure, forms, tags, speed (time to first byte and size; not field Core Web Vitals) | Real user behaviour |
| Google Ads API (Keyword Planner, account data) | Phase 5 | Search volumes as ranges, bid ranges, real account data | Competitor bids or budgets (never available) |
| Optional SERP API (e.g. DataForSEO) | Later, if needed | Repeatable results-page and ad snapshots by location | Anything about competitors' results |

The strategist must say which source a claim came from. Volumes and CPCs stay `unknown` or `estimate` (third party, dated) until Keyword Planner is connected.

## 7. API (backend ↔ interface)

```
GET    /api/health
GET    /api/projects                       list
POST   /api/projects                       {name, entry_path, objective, objective_type, market, website_url}
GET    /api/projects/{id}                  profile + facts + item counts by stage
PATCH  /api/projects/{id}
GET    /api/projects/{id}/items?stage=&kind=
PATCH  /api/items/{id}                     {status, label, title, body}
GET    /api/projects/{id}/conversations
POST   /api/projects/{id}/conversations    {title}
GET    /api/conversations/{id}/messages    rendered for display (text, tool activity, sources)
POST   /api/conversations/{id}/chat        {message, mode: standard|deep} -> text/event-stream
GET    /api/knowledge/search?q=            for the knowledge view
GET    /api/knowledge/{id}
GET    /api/stages                         the seven stages with descriptions
```

SSE events from `/chat`: `thinking` (summary text), `text` (delta), `tool_start` {name, input summary}, `tool_end` {name, ok, summary}, `item_saved` {item}, `sources` [{url, title}], `done` {usage}, `error` {message}.

## 8. Interface

One screen with three areas:
- **Left rail:** project switcher, then the seven stages. Each stage shows a count and a status dot (empty, has items, needs attention).
- **Centre:** the strategist conversation, the main surface. A Standard/Deep toggle sits next to the input. Tool activity appears as quiet inline lines ("Searching the web: car insurance SR-22 quotes"). Sources appear as small chips under an answer.
- **Right panel:** the selected stage's saved items (findings, clusters, competitors, economics, decisions, forecasts), grouped by kind, each with its label badge. Clicking an item can quote it into the chat.

Visual language: neutral greys, one accent colour, generous spacing, Inter or system font, light and dark themes. No charts until there is real data to chart.

## 9. How the seven stages connect

| Stage | Holds | Fed by |
|---|---|---|
| 01 Secure connectivity | connection profiles, verification results | Phase 5 guard; public research never waits on it |
| 02 Business & campaign understanding | project profile, facts, objective, measurement status | the conversation, `update_project`, later the account import |
| 03 Market & niche research | findings, intent clusters, competitors | web research |
| 04 Campaign & website intelligence | website issues, account diagnoses | `audit_page`, `ads_query` |
| 05 Growth & optimisation strategy | opportunities, economics, recommendations | strategist synthesis, `calculate_economics` |
| 06 Continuous learning | decisions, forecasts, experiments, lessons | `save_item`, `record_lesson`, reviews |
| 07 Control center | the interface itself | |

**Entry paths.** All three are the same project type with a different `entry_path`. The path changes the strategist's opening plan:
- `new_niche`: research first
- `website`: research plus a page audit
- `ads_account`: Stage 01, then the account import

Nothing else differs.

## 10. Stage 01: secure connectivity (Phase 5 design)

- **Connection profiles** per Ads account: required country and region, PIA region name, and Dolphin Anty profile id.
- **Verification before every protected call.** The guard asks two or three independent IP-echo services for the outbound IP, geolocates it, and compares the result with the profile. It also checks that the PIA interface or tunnel is up, through the PIA command line (`piactl get connectionstate`, `piactl get vpnip`).
- **API traffic.** Google Ads API calls run in the same process through an HTTP client that the guard re-verifies before each batch. The guard fails closed: no verification means no call, and the error says why.
- **Browser sessions** use the Dolphin Anty Local API to start the named profile. A Dolphin browser profile does not protect API requests; those rely on the system VPN route checked above.
- Only official interfaces are used: the Google Ads API with OAuth, and the PIA and Dolphin local APIs. Nothing bypasses Google's authentication.
- This runs where the VPN runs, which is Elad's PC. A cloud deployment can do research but cannot reach accounts.

## 11. Security and configuration

- Secrets come only from the environment: `ANTHROPIC_API_KEY`, `DATABASE_URL`, and later the Google Ads OAuth values.
- Locally the app listens on 127.0.0.1. A cloud deployment requires `ALLFIX_PASSWORD` (HTTP basic auth) until real accounts exist.
- Fetched web content is data. The system prompt tells the strategist that instructions inside pages are never instructions to it.

## 12. Testing

- **Unit tests:** knowledge loader and search, economics maths, tool handlers against a real local Postgres, and the migrations.
- **Strategist loop:**
  - a scripted fake model client tests the plumbing (tool dispatch, `pause_turn`, persistence)
  - a live test with a real API key runs the new-niche workflow end to end and is the acceptance test for Phase 3
- **Quality:** the 11 evaluation cases, rerun against the app, then Elad's real cases.
