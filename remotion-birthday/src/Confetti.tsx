import React, { useMemo } from "react";
import { useCurrentFrame, interpolate, random } from "remotion";
import { CANVAS, CONFETTI_COLORS } from "./theme";
import { seededRange } from "./random";

type Piece = {
  x0: number; // starting x, px
  size: number;
  colorIdx: number;
  fallSpeed: number; // px/frame
  driftAmp: number; // px, horizontal sway amplitude
  driftFreq: number; // cycles per 100 frames
  spinSpeed: number; // deg/frame
  shape: "rect" | "circle";
  startFrame: number; // staggered entry
};

/**
 * A field of falling confetti, entirely frame-driven (position is a pure
 * function of `frame`, never of wall-clock time or component lifetime) so
 * it renders identically no matter which chunk of the video a given frame
 * lands in — required for the checkpointed render to stitch back together
 * without a visible seam.
 */
export const Confetti: React.FC<{
  count?: number;
  seedOffset?: number;
  opacity?: number;
}> = ({ count = 60, seedOffset = 0, opacity = 1 }) => {
  const frame = useCurrentFrame();

  const pieces = useMemo<Piece[]>(() => {
    return new Array(count).fill(0).map((_, i) => {
      const s = seedOffset + i * 97;
      return {
        x0: seededRange(s + 1, -40, CANVAS.width + 40),
        size: seededRange(s + 2, 10, 26),
        colorIdx: Math.floor(seededRange(s + 3, 0, CONFETTI_COLORS.length)),
        fallSpeed: seededRange(s + 4, 3.5, 8.5),
        driftAmp: seededRange(s + 5, 20, 90),
        driftFreq: seededRange(s + 6, 0.6, 1.8),
        spinSpeed: seededRange(s + 7, -6, 6),
        shape: random(`shape-${s}`) > 0.5 ? "rect" : "circle",
        startFrame: Math.floor(seededRange(s + 8, 0, 40)),
      };
    });
  }, [count, seedOffset]);

  return (
    <svg
      width={CANVAS.width}
      height={CANVAS.height}
      style={{ position: "absolute", inset: 0, opacity }}
    >
      {pieces.map((p, i) => {
        const t = Math.max(0, frame - p.startFrame);
        const y = ((t * p.fallSpeed) % (CANVAS.height + 80)) - 40;
        const x = p.x0 + Math.sin((t / 100) * Math.PI * 2 * p.driftFreq) * p.driftAmp;
        const rot = t * p.spinSpeed;
        const fadeIn = interpolate(t, [0, 12], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const color = CONFETTI_COLORS[p.colorIdx];
        return (
          <g key={i} transform={`translate(${x} ${y}) rotate(${rot})`} opacity={fadeIn}>
            {p.shape === "rect" ? (
              <rect
                x={-p.size / 2}
                y={-p.size / 4}
                width={p.size}
                height={p.size / 2}
                fill={color}
                rx={2}
              />
            ) : (
              <circle r={p.size / 2.4} fill={color} />
            )}
          </g>
        );
      })}
    </svg>
  );
};
