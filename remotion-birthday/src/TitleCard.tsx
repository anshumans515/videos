import React from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { INK, GOLD, PINK, CREAM, CANVAS } from "./theme";
import { Confetti } from "./Confetti";

export const BIRTHDAY_NAME = "Rhea";

export const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scaleIn = spring({ frame, fps, config: { damping: 12, mass: 0.6 }, durationInFrames: 24 });
  const subOpacity = interpolate(frame, [16, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const subY = interpolate(frame, [16, 30], [16, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: INK }}>
      <Confetti count={70} seedOffset={0} />
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          padding: "0 80px",
        }}
      >
        <div
          style={{
            fontFamily: "Georgia, 'Times New Roman', serif",
            fontWeight: 700,
            fontSize: 46,
            letterSpacing: "0.28em",
            color: PINK,
            textTransform: "uppercase",
            marginBottom: 22,
            opacity: subOpacity,
          }}
        >
          Happy Birthday
        </div>
        <div
          style={{
            fontFamily: "Georgia, 'Times New Roman', serif",
            fontWeight: 700,
            fontSize: 128,
            lineHeight: 1.05,
            color: CREAM,
            textAlign: "center",
            transform: `scale(${scaleIn})`,
            textShadow: `0 6px 40px ${GOLD}55`,
          }}
        >
          {BIRTHDAY_NAME}
        </div>
        <div
          style={{
            marginTop: 34,
            fontFamily: "Helvetica, Arial, sans-serif",
            fontWeight: 400,
            fontSize: 34,
            color: "#ffffffcc",
            transform: `translateY(${subY}px)`,
            opacity: subOpacity,
          }}
        >
          everyone has something to say…
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const canvas = CANVAS;
