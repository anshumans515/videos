import { Composition } from "remotion";
import { BirthdayReel } from "./BirthdayReel";
import { CANVAS } from "./theme";
import { TOTAL_FRAMES } from "./segments";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="BirthdayReel"
      component={BirthdayReel}
      durationInFrames={TOTAL_FRAMES}
      fps={CANVAS.fps}
      width={CANVAS.width}
      height={CANVAS.height}
    />
  );
};
