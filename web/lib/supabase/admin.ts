import "server-only";
import { createClient } from "@supabase/supabase-js";

/** Service-role client — import only from Server Components, Server Actions, or Route Handlers. */
export function createAdminClient() {
  return createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SECRET_KEY!,
    {
      auth: {
        persistSession: false,
        autoRefreshToken: false,
      },
    }
  );
}
