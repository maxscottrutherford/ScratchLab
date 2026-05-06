import type { ExpoConfig } from "expo/config";
import * as dotenv from "dotenv";
import * as path from "path";

// Monorepo root `.env` (same variable names as root `.env.example`)
dotenv.config({ path: path.resolve(__dirname, "../.env") });

const config: ExpoConfig = {
  name: "ScratchLab",
  slug: "scratchlab",
  version: "1.0.0",
  orientation: "portrait",
  icon: "./assets/icon.png",
  userInterfaceStyle: "light",
  splash: {
    image: "./assets/splash-icon.png",
    resizeMode: "contain",
    backgroundColor: "#ffffff",
  },
  ios: {
    supportsTablet: true,
  },
  android: {
    adaptiveIcon: {
      foregroundImage: "./assets/adaptive-icon.png",
      backgroundColor: "#ffffff",
    },
  },
  web: {
    favicon: "./assets/favicon.png",
  },
  extra: {
    supabaseUrl: process.env.SUPABASE_URL ?? "",
    supabasePublishableKey: process.env.SUPABASE_PUBLISHABLE_KEY ?? "",
  },
};

export default config;
