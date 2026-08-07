import React from "react";
import { AbsoluteFill, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { SEGMENTS, TRANSITION_FRAMES } from "./segments";

// MUST go through staticFile(), not a hand-written "/timeline.mp4" string.
// Remotion's bundler copies public/ to <bundle>/public/ and serves it under
// a static base of "./public" (see getBundleStaticHash in
// @remotion/bundler) — a raw root-relative path skips that prefix entirely
// and 404s at render time, even though the exact same string works fine in
// the browser-only Studio preview (which resolves differently). Cost a
// render to track down; staticFile() is the only version-proof way to
// reference anything in public/.
const SOURCE = staticFile("timeline.mp4"); // the 14-clip concat, see build_merge.sh

/**
 * One speaker's slice, trimmed out of the single merged source file. Audio
 * ramps in/out over the transition window so the brief visual crossfade
 * doesn't also mean two people's voices layered at full volume — a plain
 * TransitionSeries only blends the video, not the audio.
 */
const Slice: React.FC<{ start: number; end: number }> = ({ start, end }) => {
  const frame = useCurrentFrame();
  const duration = end - start;
  const volume = interpolate(
    frame,
    [0, TRANSITION_FRAMES, duration - TRANSITION_FRAMES, duration],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <OffthreadVideo src={SOURCE} startFrom={start} endAt={end} volume={volume} />
    </AbsoluteFill>
  );
};

/** All 14 speakers, crossfaded in the client's fixed order. */
export const SpeakerReel: React.FC = () => {
  return (
    <TransitionSeries>
      {SEGMENTS.map((seg, i) => (
        <React.Fragment key={i}>
          <TransitionSeries.Sequence durationInFrames={seg.end - seg.start}>
            <Slice start={seg.start} end={seg.end} />
          </TransitionSeries.Sequence>
          {i < SEGMENTS.length - 1 && (
            <TransitionSeries.Transition
              presentation={fade()}
              timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
            />
          )}
        </React.Fragment>
      ))}
    </TransitionSeries>
  );
};
