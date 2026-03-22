-- ================================================
-- TABLE: predictions
-- ================================================
create table if not exists predictions (
  id uuid primary key default gen_random_uuid(),
  features jsonb not null,
  predicted_price numeric(12,2) not null,
  model_version text,
  created_at timestamptz default now()
);

create index if not exists idx_predictions_created_at
  on predictions (created_at desc);

-- ================================================
-- TABLE: model_runs
-- ================================================
create table if not exists model_runs (
  id uuid primary key default gen_random_uuid(),
  version text not null,
  rmse numeric(10,4),
  mae numeric(10,4),
  r2 numeric(6,4),
  features_used text[],
  trained_at timestamptz default now(),
  notes text
);

-- ================================================
-- ROW LEVEL SECURITY
-- ================================================
alter table predictions enable row level security;
alter table model_runs enable row level security;

-- Service role has full access (used by FastAPI backend)
create policy "service_role_all_predictions"
  on predictions
  for all
  using (true)
  with check (true);

create policy "service_role_all_model_runs"
  on model_runs
  for all
  using (true)
  with check (true);

-- NOTE: When you add user auth later, replace the above policies with:
-- using (auth.uid() = user_id) after adding a user_id uuid column
