import { createClient } from "@supabase/supabase-js";
import Constants from "expo-constants";

type Extra = {
  supabaseUrl?: string;
  supabasePublishableKey?: string;
};

const extra = Constants.expoConfig?.extra as Extra | undefined;

/** Client-side Supabase — uses `SUPABASE_PUBLISHABLE_KEY` from app config (see `app.config.ts`). */
export const supabase = createClient(
  extra?.supabaseUrl ?? "",
  extra?.supabasePublishableKey ?? ""
);
