-- ScratchLab row level security, auth sync, and course ownership helpers.
--
-- IMPORTANT: Clients using the Supabase publishable (anon) key operate as `anon` or
-- `authenticated` and are subject to these policies. Any backend or job using the
-- SUPABASE_SECRET_KEY service-role client bypasses RLS by design. Use the service
-- role only on trusted servers for privileged writes (e.g. handicap_history rows,
-- API course ingestion, admin fixes).

-- ---------------------------------------------------------------------------
-- Schema support: who created a manually entered course (RLS needs this)
-- ---------------------------------------------------------------------------
alter table public.courses
  add column if not exists created_by uuid references public.users (id) on delete set null;

comment on column public.courses.created_by is
  'Set automatically on insert for JWT users. Used to restrict updates to manual courses to their creator. Service-role inserts may leave this null (e.g. API-sourced courses).';

-- ---------------------------------------------------------------------------
-- Function: stamp course creator from auth.uid() on insert (SECURITY INVOKER)
-- ---------------------------------------------------------------------------
-- Runs as the invoking role so auth.uid() reflects the signed-in user. Service-role
-- requests typically have no JWT subject; created_by stays null unless explicitly set.
create or replace function public.set_course_created_by()
returns trigger
language plpgsql
security invoker
set search_path = public
as $$
begin
  if new.created_by is null and auth.uid() is not null then
    new.created_by := auth.uid();
  end if;
  return new;
end;
$$;

drop trigger if exists scratchlab_set_course_created_by on public.courses;

create trigger scratchlab_set_course_created_by
  before insert on public.courses
  for each row
  execute function public.set_course_created_by();

comment on function public.set_course_created_by() is
  'Fills courses.created_by from auth.uid() for authenticated inserts so manual courses have an owner for RLS.';

-- ---------------------------------------------------------------------------
-- Function + trigger: mirror auth.users -> public.users on signup
-- ---------------------------------------------------------------------------
-- SECURITY DEFINER: must insert into public.users even though RLS has no INSERT policy
-- for JWT callers. Runs as the function owner (postgres) after auth.users insert.
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.users (id, email, full_name)
  values (
    new.id,
    coalesce(new.email, ''),
    coalesce(
      new.raw_user_meta_data->>'full_name',
      new.raw_user_meta_data->>'name'
    )
  );
  return new;
end;
$$;

drop trigger if exists scratchlab_on_auth_user_created on auth.users;

create trigger scratchlab_on_auth_user_created
  after insert on auth.users
  for each row
  execute function public.handle_new_user();

comment on function public.handle_new_user() is
  'Creates the public.users profile row when a new Supabase Auth user is created (id + email from auth.users).';

-- ---------------------------------------------------------------------------
-- Enable RLS on all app tables
-- ---------------------------------------------------------------------------
alter table public.users enable row level security;
alter table public.courses enable row level security;
alter table public.holes enable row level security;
alter table public.rounds enable row level security;
alter table public.round_holes enable row level security;
alter table public.shots enable row level security;
alter table public.handicap_history enable row level security;

-- ---------------------------------------------------------------------------
-- public.users
-- ---------------------------------------------------------------------------
-- Read own profile only. Direct INSERT is denied for authenticated JWTs; new rows
-- come from handle_new_user() (SECURITY DEFINER, bypasses RLS). Service role can
-- still insert/update for support if ever needed.
create policy users_select_own
  on public.users
  for select
  to authenticated
  using (id = auth.uid());

comment on policy users_select_own on public.users is
  'Authenticated users may read only their public.users row (auth.uid() = id).';

create policy users_update_own
  on public.users
  for update
  to authenticated
  using (id = auth.uid())
  with check (id = auth.uid());

comment on policy users_update_own on public.users is
  'Authenticated users may update only their own profile; cannot change primary key to another user.';

-- ---------------------------------------------------------------------------
-- public.courses
-- ---------------------------------------------------------------------------
-- Shared read for planning rounds; authenticated inserts for manual course entry.
-- Updates limited to manual courses created by the current user. API-sourced rows
-- are not updatable via JWT (use service role for trusted backend edits).
create policy courses_select_authenticated
  on public.courses
  for select
  to authenticated
  using (true);

comment on policy courses_select_authenticated on public.courses is
  'Any authenticated user may read all courses (shared catalog).';

create policy courses_insert_authenticated
  on public.courses
  for insert
  to authenticated
  with check (true);

comment on policy courses_insert_authenticated on public.courses is
  'Authenticated users may insert courses (e.g. manual entry); created_by is set by trigger when null.';

create policy courses_update_own_manual
  on public.courses
  for update
  to authenticated
  using (source = 'manual' and created_by = auth.uid())
  with check (source = 'manual' and created_by = auth.uid());

comment on policy courses_update_own_manual on public.courses is
  'Only the creator may update a course, and only while it remains source = manual.';

-- ---------------------------------------------------------------------------
-- public.holes
-- ---------------------------------------------------------------------------
create policy holes_select_authenticated
  on public.holes
  for select
  to authenticated
  using (true);

comment on policy holes_select_authenticated on public.holes is
  'Any authenticated user may read hole data for any course.';

create policy holes_insert_authenticated
  on public.holes
  for insert
  to authenticated
  with check (true);

comment on policy holes_insert_authenticated on public.holes is
  'Authenticated users may insert holes (e.g. when defining a new course layout).';

-- ---------------------------------------------------------------------------
-- public.rounds
-- ---------------------------------------------------------------------------
create policy rounds_select_own
  on public.rounds
  for select
  to authenticated
  using (user_id = auth.uid());

comment on policy rounds_select_own on public.rounds is
  'Users may read only rounds where they are the owner (user_id = auth.uid()).';

create policy rounds_insert_own
  on public.rounds
  for insert
  to authenticated
  with check (user_id = auth.uid());

comment on policy rounds_insert_own on public.rounds is
  'Users may create rounds only for themselves (user_id must equal auth.uid()).';

create policy rounds_update_own
  on public.rounds
  for update
  to authenticated
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

comment on policy rounds_update_own on public.rounds is
  'Users may update only their own rounds; cannot reassign to another user.';

create policy rounds_delete_own
  on public.rounds
  for delete
  to authenticated
  using (user_id = auth.uid());

comment on policy rounds_delete_own on public.rounds is
  'Users may delete only their own rounds.';

-- ---------------------------------------------------------------------------
-- public.round_holes
-- ---------------------------------------------------------------------------
-- Access is derived through rounds.user_id so child rows cannot leak across accounts.
create policy round_holes_select_own_round
  on public.round_holes
  for select
  to authenticated
  using (
    exists (
      select 1
      from public.rounds r
      where r.id = round_holes.round_id
        and r.user_id = auth.uid()
    )
  );

comment on policy round_holes_select_own_round on public.round_holes is
  'Users may read round_holes only for rounds they own (join rounds on round_id, user_id = auth.uid()).';

create policy round_holes_insert_own_round
  on public.round_holes
  for insert
  to authenticated
  with check (
    exists (
      select 1
      from public.rounds r
      where r.id = round_holes.round_id
        and r.user_id = auth.uid()
    )
  );

comment on policy round_holes_insert_own_round on public.round_holes is
  'Users may insert round_holes only when the parent round belongs to them.';

create policy round_holes_update_own_round
  on public.round_holes
  for update
  to authenticated
  using (
    exists (
      select 1
      from public.rounds r
      where r.id = round_holes.round_id
        and r.user_id = auth.uid()
    )
  )
  with check (
    exists (
      select 1
      from public.rounds r
      where r.id = round_holes.round_id
        and r.user_id = auth.uid()
    )
  );

comment on policy round_holes_update_own_round on public.round_holes is
  'Users may update round_holes only under their own rounds; cannot reassign to another user round.';

create policy round_holes_delete_own_round
  on public.round_holes
  for delete
  to authenticated
  using (
    exists (
      select 1
      from public.rounds r
      where r.id = round_holes.round_id
        and r.user_id = auth.uid()
    )
  );

comment on policy round_holes_delete_own_round on public.round_holes is
  'Users may delete round_holes only for rounds they own.';

-- ---------------------------------------------------------------------------
-- public.shots
-- ---------------------------------------------------------------------------
-- Ownership is enforced through round_holes -> rounds (user_id = auth.uid()).
create policy shots_select_own_round_hole
  on public.shots
  for select
  to authenticated
  using (
    exists (
      select 1
      from public.round_holes rh
      join public.rounds r on r.id = rh.round_id
      where rh.id = shots.round_hole_id
        and r.user_id = auth.uid()
    )
  );

comment on policy shots_select_own_round_hole on public.shots is
  'Users may read shots only when the parent round_hole belongs to their round.';

create policy shots_insert_own_round_hole
  on public.shots
  for insert
  to authenticated
  with check (
    exists (
      select 1
      from public.round_holes rh
      join public.rounds r on r.id = rh.round_id
      where rh.id = shots.round_hole_id
        and r.user_id = auth.uid()
    )
  );

comment on policy shots_insert_own_round_hole on public.shots is
  'Users may insert shots only under round_holes they own (via rounds.user_id).';

create policy shots_update_own_round_hole
  on public.shots
  for update
  to authenticated
  using (
    exists (
      select 1
      from public.round_holes rh
      join public.rounds r on r.id = rh.round_id
      where rh.id = shots.round_hole_id
        and r.user_id = auth.uid()
    )
  )
  with check (
    exists (
      select 1
      from public.round_holes rh
      join public.rounds r on r.id = rh.round_id
      where rh.id = shots.round_hole_id
        and r.user_id = auth.uid()
    )
  );

comment on policy shots_update_own_round_hole on public.shots is
  'Users may update shots only under their own round_holes; cannot reassign to another user chain.';

create policy shots_delete_own_round_hole
  on public.shots
  for delete
  to authenticated
  using (
    exists (
      select 1
      from public.round_holes rh
      join public.rounds r on r.id = rh.round_id
      where rh.id = shots.round_hole_id
        and r.user_id = auth.uid()
    )
  );

comment on policy shots_delete_own_round_hole on public.shots is
  'Users may delete shots only under their own round_holes.';

-- ---------------------------------------------------------------------------
-- public.handicap_history
-- ---------------------------------------------------------------------------
-- SELECT only for JWT users. INSERT/UPDATE/DELETE are denied (no policies): trusted
-- backend uses SUPABASE_SECRET_KEY (service role), which bypasses RLS for writes
-- such as handicap_index snapshots after a round.
create policy handicap_history_select_own
  on public.handicap_history
  for select
  to authenticated
  using (user_id = auth.uid());

comment on policy handicap_history_select_own on public.handicap_history is
  'Users may read only their own handicap_history rows. Inserts/updates use service role (bypasses RLS).';

-- ---------------------------------------------------------------------------
-- Grants for PostgREST (authenticated JWT)
-- ---------------------------------------------------------------------------
grant usage on schema public to authenticated;

grant select, update on public.users to authenticated;
grant select, insert, update on public.courses to authenticated;
grant select, insert on public.holes to authenticated;
grant select, insert, update, delete on public.rounds to authenticated;
grant select, insert, update, delete on public.round_holes to authenticated;
grant select, insert, update, delete on public.shots to authenticated;
grant select on public.handicap_history to authenticated;
