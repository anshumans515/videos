import { Config } from "@remotion/cli/config";

// Render defaults. See https://www.remotion.dev/docs/config
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setConcurrency(null); // null = auto (one per core)
