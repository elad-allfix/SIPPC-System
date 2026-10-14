-- Files the user gives the strategist: Google Ads report exports (CSV/TSV) and screenshots.
-- Kept in Postgres so backups (pg_dump) carry them; deleting a file removes it for good.
create table project_files (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  name text not null,
  mime text not null,
  size_bytes integer not null,
  content bytea not null,
  created_at timestamptz not null default now()
);
create index project_files_project_idx on project_files(project_id, created_at desc);
alter table project_files enable row level security;
