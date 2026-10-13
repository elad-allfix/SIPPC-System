-- Stage 01 (secure connectivity) and the read-only Google Ads import.

-- One connection profile per project (the account it protects).
alter table connection_profiles add column login_customer_id text;
alter table connection_profiles add column updated_at timestamptz not null default now();
create unique index connection_profiles_project_idx on connection_profiles(project_id);

-- Every route verification, pass or fail, for the audit trail.
create table route_checks (
    id           bigint generated always as identity primary key,
    profile_id   uuid references connection_profiles(id) on delete cascade,
    ok           boolean not null,
    public_ip    text,
    country      text,
    region       text,
    checks       jsonb not null,
    created_at   timestamptz not null default now()
);
create index route_checks_profile_idx on route_checks(profile_id, created_at desc);

-- Imported account data. One row per resource kind per import, rows kept as returned.
create table ads_snapshots (
    id            uuid primary key default gen_random_uuid(),
    project_id    uuid not null references projects(id) on delete cascade,
    customer_id   text not null,
    taken_at      timestamptz not null default now(),
    date_range    text not null,
    status        text not null default 'running' check (status in ('running', 'done', 'failed')),
    error         text,
    summary       jsonb not null default '{}'::jsonb
);
create table ads_snapshot_rows (
    snapshot_id  uuid not null references ads_snapshots(id) on delete cascade,
    kind         text not null,
    rows         jsonb not null,
    primary key (snapshot_id, kind)
);

alter table route_checks enable row level security;
alter table ads_snapshots enable row level security;
alter table ads_snapshot_rows enable row level security;
