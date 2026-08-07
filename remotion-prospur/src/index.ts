import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

// Entry point Remotion loads. Keep this file tiny — all compositions are
// registered in Root.tsx.
registerRoot(RemotionRoot);
