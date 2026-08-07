import { AbsoluteFill } from "remotion";
import { GROUND } from "./brand";

// Placeholder composition so the studio opens to something. It intentionally
// renders nothing but the brand ground — replace it (or add siblings in
// Root.tsx) when you build a real reel.
export const Empty: React.FC = () => {
  return <AbsoluteFill style={{ backgroundColor: GROUND }} />;
};
