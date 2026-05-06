/** @type {import('next').NextConfig} */
const nextConfig = {
  // Map root `.env` names to `NEXT_PUBLIC_*` for the browser Supabase client (publishable key only).
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: process.env.SUPABASE_PUBLISHABLE_KEY,
  },
};

export default nextConfig;
