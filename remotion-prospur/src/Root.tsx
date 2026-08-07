import { Composition } from "remotion";
import { Empty } from "./Empty";
import { REEL } from "./brand";

// Register every composition here. Right now there is just the empty
// placeholder at the reel format (1080x1920 @ 30fps). Add a <Composition>
// per reel as you build them.
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Empty"
        component={Empty}
        durationInFrames={150}
        fps={REEL.fps}
        width={REEL.width}
        height={REEL.height}
      />
    </>
  );
};
