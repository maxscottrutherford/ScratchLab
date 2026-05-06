-- ScratchLab initial schema (PostgreSQL / Supabase)
-- Requires: pgcrypto (gen_random_uuid). Enabled by default on Supabase.

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------------
-- users (app profile; 1:1 with auth.users)
-- ---------------------------------------------------------------------------
create table public.users (
  id uuid primary key references auth.users (id) on delete cascade,
  email text not null,
  full_name text,
  handicap_index numeric(4, 1),
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- courses
-- ---------------------------------------------------------------------------
create table public.courses (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  location text,
  par integer not null,
  slope_rating numeric(4, 1),
  course_rating numeric(4, 1),
  source text,
  external_id text,
  created_at timestamptz not null default now(),
  constraint courses_source_check check (
    source is null or source in ('api', 'manual')
  )
);

-- ---------------------------------------------------------------------------
-- holes
-- ---------------------------------------------------------------------------
create table public.holes (
  id uuid primary key default gen_random_uuid(),
  course_id uuid not null references public.courses (id) on delete cascade,
  hole_number integer not null,
  par integer not null,
  yardage_black integer,
  yardage_blue integer,
  yardage_white integer,
  yardage_red integer
);

-- ---------------------------------------------------------------------------
-- rounds
-- ---------------------------------------------------------------------------
create table public.rounds (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users (id) on delete cascade,
  course_id uuid not null references public.courses (id) on delete restrict,
  played_at date not null,
  tees_played text,
  total_score integer,
  total_putts integer,
  fairways_hit integer,
  greens_in_regulation integer,
  handicap_differential numeric(4, 1),
  is_complete boolean not null default false,
  synced_at timestamptz,
  created_at timestamptz not null default now(),
  constraint rounds_tees_played_check check (
    tees_played is null
    or tees_played in ('black', 'blue', 'white', 'red')
  )
);

-- ---------------------------------------------------------------------------
-- round_holes
-- ---------------------------------------------------------------------------
create table public.round_holes (
  id uuid primary key default gen_random_uuid(),
  round_id uuid not null references public.rounds (id) on delete cascade,
  hole_id uuid not null references public.holes (id) on delete restrict,
  hole_number integer not null,
  par integer not null,
  score integer,
  putts integer,
  fairway_hit boolean,
  green_in_regulation boolean,
  raw_description text,
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- shots
-- ---------------------------------------------------------------------------
create table public.shots (
  id uuid primary key default gen_random_uuid(),
  round_hole_id uuid not null references public.round_holes (id) on delete cascade,
  shot_number integer not null,
  club text,
  distance_yards integer,
  lie_before text,
  lie_after text,
  strokes_gained numeric(5, 3),
  created_at timestamptz not null default now(),
  constraint shots_lie_before_check check (
    lie_before is null
    or lie_before in (
      'tee',
      'fairway',
      'rough',
      'sand',
      'green',
      'penalty',
      'unknown'
    )
  ),
  constraint shots_lie_after_check check (
    lie_after is null
    or lie_after in (
      'tee',
      'fairway',
      'rough',
      'sand',
      'green',
      'penalty',
      'unknown'
    )
  )
);

-- ---------------------------------------------------------------------------
-- handicap_history
-- ---------------------------------------------------------------------------
create table public.handicap_history (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users (id) on delete cascade,
  round_id uuid references public.rounds (id) on delete set null,
  handicap_index numeric(4, 1),
  calculated_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------
create index idx_rounds_user_id on public.rounds (user_id);
create index idx_rounds_course_id on public.rounds (course_id);
create index idx_round_holes_round_id on public.round_holes (round_id);
create index idx_shots_round_hole_id on public.shots (round_hole_id);
create index idx_handicap_history_user_id on public.handicap_history (user_id);
