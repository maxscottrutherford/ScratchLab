import { createBrowserClient } from "@supabase/ssr";

/** Browser Supabase client — uses `SUPABASE_PUBLISHABLE_KEY` via `next.config.mjs` → `NEXT_PUBLIC_*`. */
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!
  );
}
