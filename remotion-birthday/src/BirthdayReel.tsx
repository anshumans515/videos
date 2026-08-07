import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { TitleCard } from "./TitleCard";
import { SpeakerReel } from "./SpeakerReel";
import { EndCard } from "./EndCard";
import { INTRO_FRAMES, SPEAKER_SECTION_FRAMES, OUTRO_FRAMES } from "./segments";

export const BirthdayReel: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Sequence from={0} durationInFrames={INTRO_FRAMES}>
        <TitleCard />
      </Sequence>
      <Sequence from={INTRO_FRAMES} durationInFrames={SPEAKER_SECTION_FRAMES}>
        <SpeakerReel />
      </Sequence>
      <Sequence from={INTRO_FRAMES + SPEAKER_SECTION_FRAMES} durationInFrames={OUTRO_FRAMES}>
        <EndCard />
      </Sequence>
    </AbsoluteFill>
  );
};
