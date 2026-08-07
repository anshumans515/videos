import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { INK, GOLD, PINK, CREAM } from "./theme";
import { Confetti } from "./Confetti";
import { BIRTHDAY_NAME } from "./TitleCard";

export const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const heartScale = spring({ frame, fps, config: { damping: 10, mass: 0.5 }, durationInFrames: 20 });
  const lineOpacity = interpolate(frame, [10, 26], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: INK }}>
      <Confetti count={70} seedOffset={5000} />
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          padding: "0 90px",
        }}
      >
        <div style={{ fontSize: 96, transform: `scale(${heartScale})`, marginBottom: 12 }}>💛</div>
        <div
          style={{
            fontFamily: "Georgia, 'Times New Roman', serif",
            fontWeight: 700,
            fontSize: 64,
            lineHeight: 1.25,
            color: CREAM,
            textAlign: "center",
            opacity: lineOpacity,
          }}
        >
          From everyone who
          <br />
          showed up for you,
        </div>
        <div
          style={{
            marginTop: 20,
            fontFamily: "Georgia, 'Times New Roman', serif",
            fontWeight: 700,
            fontSize: 92,
            color: GOLD,
            textAlign: "center",
            opacity: lineOpacity,
          }}
        >
          Happy Birthday, {BIRTHDAY_NAME}
        </div>
        <div
          style={{
            marginTop: 30,
            width: 90,
            height: 4,
            background: PINK,
            opacity: lineOpacity,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
