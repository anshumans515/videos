# Prospur testimonials — merged

14 customer testimonial clips merged into one 1080x1920 / 30fps video.

| | |
|---|---|
| **Master** | `public/testimonials-merged.mp4` — 13:14, ~173 MB (gitignored, rebuild with the script) |
| **Shareable** | `public/testimonials-merged-web.mp4` — same cut, CRF 30, peak-corrected |
| **Build** | `./build_merge.sh <uploads-dir>` |

## Running order

Body in upload order, then the three positions the client specified:

| # | clip | who |
|---|---|---|
| 1-11 | upload order | mixed |
| 12 | `b45b340c` | young man at table — *third-last* |
| 13 | `ce447f84` | **Aseem** (Adidas sweatshirt) — *second-last* |
| 14 | `4908663c` | **Vedant** — *last* |

## Two things that would have silently wrecked this

**1. Rotation flags.** Four sources carry rotation side-data, so their stored
width/height do not describe the decoded frame:

| clip | stored | decodes to |
|---|---|---|
| 05, 12 | 1024x576 | **576x1024** (portrait) |
| 11 | 576x1024 | **1024x576** (landscape) |
| 02, 07, 10 | 1024x576 | 1024x576, but flagged rot=-180 |

Branching on ffprobe's stored dimensions would have pushed three clips
through the wrong path — portrait clips squashed into a landscape treatment
and vice versa. The script decodes a probe frame and measures *that* instead.

**2. Mixed loudness.** Sources ranged -16.9 to -38.3 LUFS — a 21 dB spread.
Concatenated raw, the viewer rides the volume knob for 13 minutes. Every
segment is normalised to -14 LUFS before the concat, and the final pass
re-limits to keep true peak under -1.5 dBTP (the straight concat came out at
-0.4 dBFS, hot enough to clip on some players).

## Why landscape clips are not centre-cropped

Ten of the 14 are landscape. Cropping a 1024x576 frame to 9:16 needs a
324px-wide slice — throwing away 68% of the width and cutting off the
speakers' hands, which several of them talk with. They sit in a centred band
over a blurred, darkened copy of themselves instead: nobody gets cropped, and
the frame stays full.

## Before this is published

- **Compliance is unreviewed.** These are customer testimonials for an
  AMFI-registered Mutual Fund Distributor. If any speaker states returns,
  performance, or a specific gain, that clip cannot go out as-is
  (PLAYBOOK.md §2). Nobody has transcribed these yet — do that before
  publishing, not after.
- **No compliance strip is burned in.** The merge is raw. Anything published
  needs the strip for its full duration plus the caption disclaimer (§2, §12).
- 13:14 is not a Reels length. This is a website / internal-review asset. A
  Reels cut would need soundbites pulled per speaker.
