# Archetype 1 · talking-head recut

Single person speaking to camera. Skill: `/talking-head-recut`.
See PLAYBOOK.md §4, §6, §9.

## Inputs

Drop these into the project folder (copied from this template) before
running the assembler:

- `input-video.mp4` — the repaired base clip, built per PLAYBOOK.md §7
  (audio fixed, brightness lift applied, dense keyframes). **Not** the raw
  source file.
- `transcript.json` *(optional)* — Whisper word-level output, generated
  **after** the audio repair pass (never transcribe an unrepaired quiet
  clip — §3). Shape:
  ```json
  [{"word": "So", "start": 2.01, "end": 2.34}, ...]
  ```
- `config.json` *(optional)* — per-clip overrides:
  ```json
  {
    "duration": 24,
    "head_position": "standing",
    "kicker": "MUTUAL FUNDS, EXPLAINED",
    "title_lines": ["Why one fund", "isn't a plan"],
    "name": "Vedant",
    "role": "Prospur"
  }
  ```
  `head_position` is `"standing"` (head y ~470–700) or `"seated"` (head y
  ~900) — it drives both the card safe-zone and the scrim height (§5).

Neither file is required — `python3 assemble.py` with no inputs renders a
demo comp so the template is verifiable on its own.

## What the assembler builds

- Background legibility scrim tuned to `head_position` (§5, `card-scrim.html`
  reference in `public/cards/`)
- Kicker chip + kinetic title (first ~4s)
- Lower-third name card (first ~5.5s, positioned inside the safe-zone)
- Karaoke word-pop captions, chunked from `transcript.json`, with
  `CAP_OFFSET = 0.34` applied to correct Whisper's early word-start bias (§6)
- Sticky brand mark (top-right, white-on-dark via CSS filter)
- Compliance strip, full duration, bottom-of-frame (§2)

All timed elements carry `class="clip"` on their own `data-track-index`;
GSAP animates inner wrapper divs, never the `.clip` element itself, per the
HyperFrames lint rules in PLAYBOOK.md §9.

## Editing loop

```bash
python3 assemble.py
npx hyperframes lint public
npx hyperframes snapshot public --at 2,8,15,22
PRODUCER_BROWSER_GPU_MODE=hardware \
  npx hyperframes render public --skill=talking-head-recut -o output.mp4 --fps 30
```
