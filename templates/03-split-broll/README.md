# Archetype 3 · split-screen B-roll

Silent B-roll, vertical split, kinetic text overlay. Skill: `/general-video`.
See PLAYBOOK.md §4, §8.

## Build order

1. **Composite the video first**, outside HyperFrames, with `build_clips.sh`
   (implements the exact ffmpeg recipe in PLAYBOOK.md §8 — two source clips
   → 540×1920 halves → hstack → mux music bed):

   ```bash
   ./build_clips.sh saver-source.mp4 spender-source.mp4 music_bed.m4a
   ```

   This writes `public/input-video.mp4` as a single pre-composited
   split-screen clip with the music bed already muxed in. **Retune the
   `crop iw*0.22` / `iw*0.28` offsets** for your source so each half is
   centered on the subject, not the background — and if a source has
   multiple people, isolate one person per half and slow-loop a short clean
   segment rather than trying to cover the full duration from raw footage
   (character-consistency note in §8).

2. Then build the kinetic overlay:

   ```bash
   python3 assemble.py
   ```

   Optional `config.json`:
   ```json
   {
     "duration": 25.5,
     "left_label": "SAVER", "right_label": "SPENDER",
     "hook_lines": ["Same income.", "Different habits."],
     "counter": {"enabled": true, "target": 37, "label": "days of consistency", "note": "ILLUSTRATIVE ONLY"},
     "jar": {"enabled": true, "fill_pct": 0.7}
   }
   ```
   Omit it and the assembler renders the demo SAVER│SPENDER script so the
   template is verifiable without any source media.

## What the overlay builds

- Divider glow (6px white bar, brand-green box-shadow) at the split
- Paired label chips, one per half
- Kinetic word-pop hook over a dark scrim in the first ~3s
- Optional running counter (`counter`) — an illustrative motif (e.g. a
  streak count), never a fund return figure; auto-labeled `ILLUSTRATIVE
  ONLY` unless overridden
- Optional jar-fill SVG (`jar`) — same illustrative-only rule
- Sticky brand mark + compliance strip, full duration

## Editing loop

```bash
npx hyperframes lint public
npx hyperframes snapshot public --at 2,8,15,22
PRODUCER_BROWSER_GPU_MODE=hardware \
  npx hyperframes render public --skill=general-video -o output.mp4 --fps 30
```
