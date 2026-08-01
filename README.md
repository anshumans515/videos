# Prospur Reel System

Tooling and templates for producing Prospur's Instagram Reels in
[HyperFrames](https://www.npmjs.com/package/hyperframes). Read
[`PLAYBOOK.md`](./PLAYBOOK.md) in full before touching any composition — it is
the single source of truth for brand tokens, compliance copy, safe-zones,
audio repair, and the HyperFrames lint rules this repo is built around.

## Layout

```
PLAYBOOK.md                 the full playbook (read this first)
assets/
  fonts/                    Inter + Source Serif 4 (bundled, never fetched over network)
  prospur-logo.png          880×168 wordmark w/ alpha (see assets/README.md)
reference-renders/          example output MP4s referenced by the playbook
templates/
  01-talking-head/          Archetype 1 — single-person spoken reel
  02-faceless-explainer/    Archetype 2 — no footage, pure text/motion
  03-split-broll/           Archetype 3 — silent split-screen B-roll
  04-cover/                 Archetype 4 — still Reels cover / thumbnail
.claude/skills/             project skills matching each archetype
  talking-head-recut/
  faceless-explainer/
  general-video/
  motion-graphics/
```

## Starting a new reel

1. Match the source material to an archetype — see PLAYBOOK.md §4 / §11.
2. Copy the matching `templates/0N-*/` directory into a new project folder
   (e.g. `my-reel/`), keeping its internal structure intact.
3. Drop source media into the new project folder (`in.mp4`, `music_bed.m4a`,
   `transcript.json`, etc. as required by that template's README).
4. Run the standard editing loop (PLAYBOOK.md §10):

   ```bash
   cd my-reel
   python3 assemble.py
   npx hyperframes lint public
   npx hyperframes snapshot public --at 2,8,15,22
   PRODUCER_BROWSER_GPU_MODE=hardware \
     npx hyperframes render public --skill=<matching-skill> -o output.mp4 --fps 30
   ```

Every template's `assemble.py` is self-contained (brand tokens, compliance
strip markup, and HyperFrames-lint-safe scaffolding are inlined) so a cloned
template never depends on the rest of this repo at render time.

## Compliance

Every single reel this repo produces must carry the on-screen compliance
strip for its full duration, and every caption drafted for it must carry the
matching disclaimer text. See PLAYBOOK.md §2 and §12 — this is non-negotiable
and is enforced structurally in each template (the compliance strip node has
`data-duration` equal to the full composition length).
