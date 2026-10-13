-- Subscription backend (Claude Agent SDK): which backend a conversation uses, its
-- agent session id, and a copy of the agent's transcript so a conversation can be
-- resumed on another machine or after local files are cleaned up.
alter table conversations add column backend text not null default 'api';
alter table conversations add column agent_session_id text;

create table agent_transcripts (
    seq          bigint generated always as identity primary key,
    project_key  text not null,
    session_id   text not null,
    subpath      text not null default '',
    uuid         text,
    entry        jsonb not null,
    created_at   timestamptz not null default now()
);
create index agent_transcripts_session_idx on agent_transcripts(session_id, subpath, seq);
create unique index agent_transcripts_uuid_idx on agent_transcripts(session_id, subpath, uuid) where uuid is not null;
alter table agent_transcripts enable row level security;
