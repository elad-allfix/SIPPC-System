-- AllFix initial schema. Plain Postgres (13+); no extensions required.

create table projects (
    id              uuid primary key default gen_random_uuid(),
    name            text not null,
    entry_path      text not null default 'new_niche'
                    check (entry_path in ('new_niche', 'website', 'ads_account')),
    objective       text not null default '',
    objective_type  text not null default 'unknown'
                    check (objective_type in ('profit', 'leads', 'sales', 'traffic', 'awareness', 'unknown')),
    country         text,
    region          text,
    language        text,
    website_url     text,
    notes           text not null default '',
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

-- Business facts with provenance (margin, close rate, capacity, ...).
create table project_facts (
    project_id  uuid not null references projects(id) on delete cascade,
    key         text not null,
    value       text not null,
    label       text not null default 'assumption'
                check (label in ('verified', 'observed', 'estimate', 'assumption', 'hypothesis', 'unknown')),
    source      text not null default '',
    updated_at  timestamptz not null default now(),
    primary key (project_id, key)
);

create table conversations (
    id          uuid primary key default gen_random_uuid(),
    project_id  uuid not null references projects(id) on delete cascade,
    title       text not null default 'New conversation',
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);
create index conversations_project_idx on conversations(project_id, updated_at desc);

-- Exact API message content, append-only, so thinking blocks stay valid.
create table messages (
    id               bigint generated always as identity primary key,
    conversation_id  uuid not null references conversations(id) on delete cascade,
    seq              integer not null,
    role             text not null check (role in ('user', 'assistant', 'system')),
    content          jsonb not null,
    model            text,
    mode             text,
    usage            jsonb,
    created_at       timestamptz not null default now(),
    unique (conversation_id, seq)
);

-- Everything the strategist saves: findings, intent clusters, competitors,
-- economics, website issues, opportunities, risks, decisions, forecasts,
-- experiments and open questions.
create table items (
    id             uuid primary key default gen_random_uuid(),
    project_id     uuid not null references projects(id) on delete cascade,
    stage          smallint not null check (stage between 1 and 7),
    kind           text not null check (kind in (
                     'finding', 'intent_cluster', 'competitor', 'economics', 'website_issue',
                     'opportunity', 'risk', 'decision', 'forecast', 'experiment', 'question')),
    title          text not null,
    body           text not null default '',
    data           jsonb not null default '{}'::jsonb,
    label          text not null default 'hypothesis'
                   check (label in ('verified', 'observed', 'estimate', 'assumption', 'hypothesis', 'unknown')),
    confidence     text not null default 'medium' check (confidence in ('high', 'medium', 'low')),
    sources        jsonb not null default '[]'::jsonb,
    status         text not null default 'open'
                   check (status in ('open', 'confirmed', 'refuted', 'done', 'dropped', 'superseded')),
    superseded_by  uuid references items(id),
    conversation_id uuid references conversations(id) on delete set null,
    created_at     timestamptz not null default now(),
    updated_at     timestamptz not null default now()
);
create index items_project_stage_idx on items(project_id, stage, created_at desc);
create index items_project_kind_idx on items(project_id, kind);

-- Corrections and lessons, optionally shared across projects.
create table lessons (
    id              uuid primary key default gen_random_uuid(),
    project_id      uuid references projects(id) on delete cascade,
    what_was_wrong  text not null,
    correction      text not null,
    applies_to      text not null default '',
    kb_entry_ids    text[] not null default '{}',
    created_at      timestamptz not null default now()
);

-- The expert knowledge base, indexed for full-text search.
create table kb_entries (
    id             text primary key,
    file           text not null,
    area           text not null,
    title          text not null,
    claim          text not null default '',
    body           text not null,
    evidence_type  text,
    confidence     text,
    changed        boolean not null default false,
    search         tsvector generated always as (
                     setweight(to_tsvector('english', coalesce(id, '') || ' ' || coalesce(title, '')), 'A') ||
                     setweight(to_tsvector('english', coalesce(claim, '')), 'B') ||
                     setweight(to_tsvector('english', coalesce(body, '')), 'C')
                   ) stored
);
create index kb_entries_search_idx on kb_entries using gin(search);

-- Playbooks, relationship map, readiness notes, demo research.
create table kb_documents (
    slug    text primary key,
    title   text not null,
    kind    text not null,
    body    text not null,
    search  tsvector generated always as (
              setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
              setweight(to_tsvector('english', coalesce(body, '')), 'C')
            ) stored
);
create index kb_documents_search_idx on kb_documents using gin(search);

-- Stage 01 (Phase 5): one profile per protected account.
create table connection_profiles (
    id                  uuid primary key default gen_random_uuid(),
    project_id          uuid not null references projects(id) on delete cascade,
    ads_customer_id     text,
    required_country    text not null,
    required_region     text,
    vpn_profile         text,
    dolphin_profile_id  text,
    last_verified_at    timestamptz,
    last_result         jsonb,
    created_at          timestamptz not null default now()
);

-- Scheduled rounds (Phase 6).
create table runs (
    id           uuid primary key default gen_random_uuid(),
    project_id   uuid references projects(id) on delete cascade,
    kind         text not null,
    status       text not null default 'running',
    summary      text not null default '',
    started_at   timestamptz not null default now(),
    finished_at  timestamptz
);
