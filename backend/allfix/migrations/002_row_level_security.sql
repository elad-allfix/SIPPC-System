-- Turn on row level security with no policies. AllFix connects as the table owner,
-- which bypasses RLS, so the app is unaffected. Any other role (for example the
-- public API roles a hosted Postgres such as Supabase exposes) gets no rows.
alter table schema_migrations enable row level security;
alter table projects enable row level security;
alter table project_facts enable row level security;
alter table conversations enable row level security;
alter table messages enable row level security;
alter table items enable row level security;
alter table lessons enable row level security;
alter table kb_entries enable row level security;
alter table kb_documents enable row level security;
alter table connection_profiles enable row level security;
alter table runs enable row level security;
