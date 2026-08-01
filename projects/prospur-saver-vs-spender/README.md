# SAVER vs SPENDER — Prospur Instagram Reel

Archetype 3 (split-screen B-roll), adapted for a source that is already a
**top/bottom** split rather than the left/right split the stock template
assumes. See `PLAYBOOK.md` §4, §8, §9.

| | |
|---|---|
| **Output** | `output.mp4` — 1080×1920, 30 fps, 25.3 s (render master, ~55 MB) |
| **For upload** | `output-ig.mp4` — same thing at CRF 23, ~22 MB |
| **Cover** | `../prospur-cover/cover.png` |
| **Caption** | `caption.md` |
| **Audio** | −15.2 LUFS integrated, −1.9 dBFS true peak |
| **Cast** | Anshuman (blue shirt) = plans first · Vedant (white shirt) = spends first |

The film grain is high-frequency detail, so it costs real bitrate — the
master lands around 55 MB for 25 seconds. `output-ig.mp4` is a straight CRF 23
re-encode of it (audio stream copied, not re-encoded) and is what to actually
upload; Instagram re-encodes on ingest anyway, so the extra 30 MB buys
nothing downstream.

## Rebuild

```bash
./build_base.sh /path/to/source.mp4     # -> public/input-video.mp4
python3 assemble.py                     # -> public/index.html
npx hyperframes lint public             # 0 errors required
npx hyperframes snapshot public --at 2.4,8,13,18,21.6,24.3
npx hyperframes render public --skill=general-video -o output.mp4 --fps 30
```

Add `PRODUCER_BROWSER_GPU_MODE=hardware` to the render on a machine with a
usable GPU. Without one it falls back to software rasterisation and a 25 s
reel takes ~7 minutes rather than ~90 s.

## What the source was, and what had to be fixed

The source is a 2160×3240 clip that is **already composited** as a stacked
comparison — Anshuman on top, Vedant below — running five scenes:

| Scene | Cut | Beat |
|---|---|---|
| 1 | 0 – 6.43 s | Both walk out of a café with the same coffee |
| 2 | 6.43 – 10.50 s | Deliveries: one parcel vs a pile |
| 3 | 10.50 – 15.67 s | Desk: one item vs four |
| 4 | 15.67 – 20.43 s | Headphones: considered vs bought |
| 5 | 20.43 – 25.27 s | SAVINGS jar: filling vs empty |

Three problems `build_base.sh` fixes:

1. **Aspect.** 2160×3240 is 2:3, Reels is 9:16. Cropping *vertically* keeps
   the full source width (only 72 px off each half, 4.4%), which matters
   because every story beat — parcels, snacks, jars — is spread
   horizontally. A side crop would have cut them.

2. **The halves swap.** At the last cut (20.4333 s) the source puts Vedant on
   top. Persistent SAVER/SPENDER labels would then be pointing at the wrong
   person, so the final segment is re-stacked in reverse (PLAYBOOK §8,
   character consistency). This is the single most important fix in the
   build — without it the payoff scene reads backwards.

3. **Audio.** Ambient only, and very quiet: −29.5 LUFS integrated, −10.8 dBFS
   peak. Repaired with the §7 chain (denoise runs harder than default since
   there is no speech to protect). Loudness lands at −15.2 LUFS; the
   two-pass target aims at −2.0 dBTP because the AAC encode pushes peaks
   back up roughly half a dB.

## Layout, and why the chrome sits where it does

```
y    0 – 1548   video block (two halves of 774, seam at y=774)
y 1548 – 1658   compliance strip
y 1658 – 1920   brand band (Prospur mark + prospur.in)
```

The video is **not** full-bleed, deliberately. Instagram's in-feed UI covers
roughly the bottom 250 px, so a compliance strip anchored to the bottom of a
full-bleed frame gets cropped out in feed — and PLAYBOOK §2 makes that strip
non-negotiable for the reel's full duration. Floating it mid-frame instead
(the §2 "lift to y=1500" remedy) was tried and rejected: at that height it
lands directly on the parcels in scene 2, the snack line-up in scene 3, and
Vedant's SAVINGS jar in scene 5. Shrinking the video to 1548 and giving the
strip its own band puts it fully above the UI band with nothing overlaid on
the footage.

Everything drawn *over* the video sits on the seam — the one strip of frame
that is never a face, because it is where two separate shots join:

- **left of seam** — name chips whose second line changes per scene
  (`PLANS FIRST` → `ONE PARCEL` → `ONE ITEM` → `SLEPT ON IT` → `SAVES FIRST`)
- **right of seam** — the scene caption
- **below-right** — a small Prospur watermark, so the brand is still visible
  in-feed when the bottom band is covered

## Compliance notes

- Compliance strip runs the full duration, verbatim per §2, on its own plate.
- **No rupee figures anywhere.** The contrast is carried entirely by what is
  physically on screen — parcel counts, desk clutter, jar level — so the reel
  never needs a masked or illustrative amount at all.
- Chip copy states only what is visible. Scene 3 says `ONE ITEM` / `FOUR
  ITEMS`, not "snacks": the spender side is a protein bar, a coffee cup, a
  bottle and an energy-bites pack, and only two of those are snacks.
- CTA is non-directive — "Want to understand where yours goes?" — and
  "Start your SIP" is the §2-approved generic CTA.
- The caption in `caption.md` carries the full disclaimer block, which §12
  requires independently of the on-screen strip.

## The cinematic layer, and three traps in it

On top of the storytelling chrome the reel runs a base layer: a per-half
colour grade (cool green on the saver, warm amber on the spender), a
vignette, film grain, a bloom on each scene cut with a pulse through the
divider, and a letterbox that rides in with the hook. `CINEMA=0 python3
assemble.py` builds without the three full-frame layers, which is the fastest
way to bisect a rendering problem.

Three things cost a render each to find. Do not reintroduce them:

1. **Never call `hold()` on a static always-on layer.** It sets `opacity: 1`,
   which silently overrides whatever alpha the CSS intends — this is how the
   grain ended up painting at full strength over the footage instead of at
   0.055. A `.clip` element is already visible inside its own window, so
   those layers need no GSAP at all.

2. **Grain comes from a pre-baked noise tile** (`public/brand/noise.png`,
   192px, repeated), not an inline SVG `feTurbulence`. The filter version is
   catastrophically slow under software rasterisation: it took this 25 s
   render past 40 minutes with no end in sight, versus 8m45s for the tile.
   Visually they are indistinguishable at 5% opacity.

3. **`mix-blend-mode` over the `<video>` is not safe here.** Chromium
   promotes the video to its own compositing layer and a blended element
   above it composites *without* that layer in its backdrop. Plain alpha only.

### The snapshot previewer lies about early frames

`hyperframes snapshot` renders the video block as flat white for any
timestamp before ~20.4 s in this environment, and `hyperframes validate`
inherits the same blank backdrop — which is why its contrast warnings read
1.7:1 for white caption text. **The rendered MP4 is correct at every
timestamp**; this was verified by decoding real frames out of `output.mp4`
with ffmpeg. Bisecting confirmed it is not the tints, vignette or grain
(removing all three changes nothing) and not GOP density (the base video has
clean 1-second keyframes throughout).

So: use snapshots to check layout and composition, but verify anything about
the footage itself against decoded frames of the render —

```bash
ffmpeg -ss 13 -i output.mp4 -frames:v 1 -y /tmp/check.jpg
```

## Known gaps

- **`public/brand/prospur-logo.png` is missing.** The artwork was supplied as
  an inline chat image rather than a file, and prospur.in is blocked by this
  environment's proxy, so `assemble.py` falls back to a plain green mark.
  Drop the real PNG at that path and re-run `assemble.py` — it swaps
  automatically, no code change. Prefer a transparent, white/knockout
  version: it sits on the dark brand band and on the seam over footage. No
  "Prospur" text is set beside it, since the logo is itself a wordmark.
- **No music bed.** The reel ships with repaired room tone. Drop a licensed
  `music_bed.m4a` beside `build_base.sh` and re-run it to swap. For reach,
  adding trending audio in-app is usually the stronger play — there is no
  dialogue to protect.
