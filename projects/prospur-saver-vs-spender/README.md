# SAVER vs SPENDER — Prospur Instagram Reel

Archetype 3 (split-screen B-roll), adapted for a source that is already a
**top/bottom** split rather than the left/right split the stock template
assumes. See `PLAYBOOK.md` §4, §8, §9.

| | |
|---|---|
| **Output** | `output.mp4` — 1080×1920, 30 fps, 25.3 s |
| **Cover** | `../prospur-cover/public/snapshots/frame-00-at-0s.png` |
| **Caption** | `caption.md` |
| **Audio** | −15.2 LUFS integrated, −1.9 dBFS true peak |
| **Cast** | Anshuman (blue shirt) = plans first · Vedant (white shirt) = spends first |

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

## Known gaps

- **`public/brand/prospur-logo.png` is missing.** The real wordmark could not
  be fetched in this environment, so `assemble.py` falls back to a
  typographic lockup. Drop the real 880×168 PNG at that path and re-run
  `assemble.py` — it swaps automatically, no code change.
- **No music bed.** The reel ships with repaired room tone. Drop a licensed
  `music_bed.m4a` beside `build_base.sh` and re-run it to swap. For reach,
  adding trending audio in-app is usually the stronger play — there is no
  dialogue to protect.
