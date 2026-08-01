---
name: faceless-explainer
description: Build a no-footage, text-and-motion explainer Reel for Prospur from a topic or script — editorial serif type, kinetic bars/charts/circles, warm-paper background. Use when the user gives a topic or brief with no source video and wants an explainer Reel.
---

# faceless-explainer

Builds Archetype 2 reels (PLAYBOOK.md §4). Read `/PLAYBOOK.md` in full
before starting — this skill assumes its rules (§1–§2, §9).

## Steps

1. **Confirm the archetype.** No source footage — a topic, brief, or
   script only. If there's an MP4 involved, use a different archetype
   (PLAYBOOK §11).

2. **Draft the scene script** as a beat sheet, not prose: 3-6 scenes, each
   either `text` (a kinetic headline), `bars` (a labeled bar chart), or
   `circle` (an animated donut/ring). Keep each scene under ~5s. See
   `templates/02-faceless-explainer/README.md` for the exact `config.json`
   scene schema.

3. **Compliance-check the script before building anything**:
   - No invented return figures, ever.
   - Any numeric `bars`/`circle` value must be illustrative of a
     *structure* (an allocation split, a process), not performance —
     label it `ILLUSTRATIVE ONLY` (auto-applied to `bars` scenes unless
     overridden).
   - No named schemes/AMCs.
   - Non-directive phrasing throughout ("may suit", not "you should").

4. **Set up the project**: copy `templates/02-faceless-explainer/` to a new
   project folder, write `config.json` with the scene list.

5. Run the standard editing loop (PLAYBOOK §10):
   ```bash
   python3 assemble.py
   npx hyperframes lint public
   npx hyperframes snapshot public --at 2,8,15,22
   PRODUCER_BROWSER_GPU_MODE=hardware \
     npx hyperframes render public --skill=faceless-explainer -o output.mp4 --fps 30
   ```

## Checks before calling it done

- [ ] Compliance strip visible for the entire duration (§2)
- [ ] No invented figures; illustrative numbers are labeled or masked (§2)
- [ ] Scene crossfades don't collide (`data-track-index` alternates between
      adjacent scenes, per §9.5)
- [ ] `npx hyperframes lint public` returns 0 errors
