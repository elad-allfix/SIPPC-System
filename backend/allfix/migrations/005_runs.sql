-- Phase 6: scheduled rounds. One row per project, kind and day; results kept as data.
alter table runs add column run_date date not null default current_date;
alter table runs add column attention boolean not null default false;
alter table runs add column data jsonb not null default '{}'::jsonb;
alter table runs add column error text;
alter table runs add constraint runs_status_check check (status in ('running', 'done', 'failed', 'skipped'));
create unique index runs_project_kind_day_idx on runs(project_id, kind, run_date);
create index runs_recent_idx on runs(project_id, started_at desc);
