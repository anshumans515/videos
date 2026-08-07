// Frame boundaries of each of the 14 speaker clips inside the pre-merged
// source video (public/timeline.mp4 — a straight ffmpeg concat of the 14
// uploads, already 1080x1920/30fps, in the client's fixed running order:
// upload order for the body, then the named tail — Aseem 2nd-last, Vedant
// last). Measured directly off the merged file's segment durations, not
// estimated.
//
// TransitionSeries below trims each speaker's slice out of this ONE source
// file via startFrom/endAt rather than needing 14 separate video assets.
export const FPS = 30;

export type Segment = { start: number; end: number; label?: string };

export const SEGMENTS: Segment[] = [
  { start: 0, end: 2104 }, // 01  0:00.0 - 1:10.1
  { start: 2104, end: 3847 }, // 02  1:10.1 - 2:08.2
  { start: 3847, end: 4285 }, // 03  2:08.2 - 2:22.8
  { start: 4285, end: 5320 }, // 04  2:22.8 - 2:57.3
  { start: 5320, end: 7177 }, // 05  2:57.3 - 3:59.2
  { start: 7177, end: 8194 }, // 06  3:59.2 - 4:33.1
  { start: 8194, end: 10777 }, // 07  4:33.1 - 5:59.2
  { start: 10777, end: 12199 }, // 08  5:59.2 - 6:46.6
  { start: 12199, end: 13589 }, // 09  6:46.6 - 7:32.9
  { start: 13589, end: 14754 }, // 10  7:32.9 - 8:11.8
  { start: 14754, end: 17907 }, // 11  8:11.8 - 9:56.9
  { start: 17907, end: 19375 }, // 12  9:56.9 - 10:45.8
  { start: 19375, end: 21739, label: "Aseem" }, // 13  10:45.8 - 12:04.6
  { start: 21739, end: 23821, label: "Vedant" }, // 14  12:04.6 - 13:14.0
];

export const TIMELINE_FRAMES = SEGMENTS[SEGMENTS.length - 1].end;

// Crossfade length between consecutive speakers. TransitionSeries overlaps
// this many frames between each pair of Sequences (total runtime shrinks by
// transitionFrames * (count-1) versus a hard-cut concat) — kept short so it
// reads as a polish, not a scene change, and so two people's voices only
// briefly overlap.
export const TRANSITION_FRAMES = 12; // 0.4s @ 30fps

// Bookend lengths, in frames.
export const INTRO_FRAMES = 105; // 3.5s
export const OUTRO_FRAMES = 150; // 5s

// TransitionSeries overlaps TRANSITION_FRAMES between each adjacent pair, so
// the assembled speaker section is shorter than the raw sum of clip lengths
// by (count - 1) transitions. Compute it here rather than hardcode it, so
// changing TRANSITION_FRAMES or the segment list can't silently desync the
// total composition length from what TransitionSeries actually produces.
export const SPEAKER_SECTION_FRAMES =
  TIMELINE_FRAMES - TRANSITION_FRAMES * (SEGMENTS.length - 1);

export const TOTAL_FRAMES = INTRO_FRAMES + SPEAKER_SECTION_FRAMES + OUTRO_FRAMES;
