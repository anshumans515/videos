# remotion-birthday

A birthday compilation for a personal (non-Prospur) video — 14 talking-head
messages, crossfaded together with an animated title and end card, built in
Remotion `4.0.505`.

**Not Prospur content.** Separate palette (`src/theme.ts` — plum/gold/pink,
not the Prospur green/amber system), no compliance strip, no logo.

## Status

| | |
|---|---|
| Scaffold, transitions, confetti | ✅ built, spot-rendered, verified against decoded frames |
| Title card / end card | 🚧 blocked — placeholder name (`src/TitleCard.tsx`) until confirmed |
| Full 13:17 render | not started — waiting on the name above |

## Setup

```bash
cd remotion-birthday
npm install                                            # pinned exact: remotion 4.0.505
cp ../projects/prospur-testimonials/public/testimonials-merged.mp4 public/timeline.mp4
npm run studio
```

The merged source isn't in git (172MB, past what belongs in a repo) — build
it first from `../projects/prospur-testimonials/` (`./build_merge.sh`), then
copy it in as above. **Use a real copy, not a symlink** — see the note below.

## Layout

```
src/
  index.ts          registerRoot entry
  Root.tsx           registers the BirthdayReel composition
  BirthdayReel.tsx    intro Sequence -> SpeakerReel Sequence -> outro Sequence
  SpeakerReel.tsx      TransitionSeries over all 14 speakers
  TitleCard.tsx / EndCard.tsx    the two bookends (share BIRTHDAY_NAME)
  Confetti.tsx        deterministic particle field (see random.ts)
  random.ts           seeded PRNG — never Math.random(), see below
  segments.ts         measured frame boundaries for each of the 14 clips
  theme.ts            this project's own palette + the 1080x1920/30fps canvas
```

## Two things that cost a render each to find

**1. `staticFile()` is not optional.** `SpeakerReel.tsx` originally
referenced the source video as a hand-written `"/timeline.mp4"` string. That
works in the Studio preview and 404s during an actual render — Remotion's
bundler copies `public/` to `<bundle>/public/` and serves it under a static
base of `./public` (see `getBundleStaticHash` in `@remotion/bundler`); a raw
root-relative path skips that prefix. Always use `staticFile("timeline.mp4")`
for anything under `public/`, never a literal string.

**2. Confetti must be frame-deterministic, not `Math.random()`-driven.** The
full render runs in checkpointed chunks (see below) so a container restart
only loses the current chunk, not the whole ~5 hours. If each chunk's
confetti were seeded by wall-clock time or React state, particles would jump
at every chunk boundary. `random.ts`'s `mulberry32` gives every particle a
stable seed derived from its index, so frame N always looks identical no
matter which process rendered it.

## Rendering (do this in checkpointed chunks, not one run)

This sandbox renders in software (no GPU) — a 25s reel takes ~9 minutes here,
and this video is 13:17 (23,920 frames), so a single unbroken render is
**4-5 hours**. The container has already restarted once mid-build today. Do
not run one `remotion render` over the whole timeline — render in chunks of
a few thousand frames each to `chunks/chunk_NN.mp4`, then stitch with the
ffmpeg concat demuxer (`-c copy`, since every chunk shares identical
codec/settings — instant, lossless). A restart then costs one chunk, not the
run.

```bash
CHROME=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell  # this sandbox only
npx remotion render BirthdayReel chunks/chunk_00.mp4 --browser-executable="$CHROME" --frames=0-2999
# ...repeat per chunk...
```

On a normal machine with a GPU, skip all of this and just run
`npm run render BirthdayReel out/birthday.mp4` — Remotion downloads its own
Chrome and renders directly; the chunking and `--browser-executable` override
above exist only because this sandbox's egress allowlist blocks that
download and has no GPU.

## Before finishing

- Swap `BIRTHDAY_NAME` in `src/TitleCard.tsx` — it's currently the loud
  `🚧 NAME_TBD 🚧` placeholder on purpose, so this can't render to a client by
  accident. `EndCard.tsx` imports the same constant, so one edit updates both.
