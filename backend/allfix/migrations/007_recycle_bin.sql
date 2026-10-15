-- Recycle bin: a deleted project keeps its data until it is deleted forever from the bin.
alter table projects add column if not exists deleted_at timestamptz;
