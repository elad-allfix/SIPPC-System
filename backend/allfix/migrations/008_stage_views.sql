-- A short visual summary of each stage, written by the model from the stage's saved items.
-- The fingerprint records which items it was written from, so a changed stage gets a new one.
create table if not exists stage_views (
  project_id uuid not null references projects(id) on delete cascade,
  stage smallint not null,
  fingerprint text not null,
  view jsonb not null,
  model text,
  created_at timestamptz not null default now(),
  primary key (project_id, stage)
);
alter table stage_views enable row level security;
