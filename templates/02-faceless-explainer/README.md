# Archetype 2 · faceless explainer

No footage — pure editorial serif type and kinetic motion on a warm-paper
background. Skill: `/faceless-explainer`. See PLAYBOOK.md §4.

## Input

No source video. Everything comes from `config.json`'s `scenes` array
(optional — omit it and `python3 assemble.py` renders a demo script on a
flexi-cap explainer so the template is verifiable on its own):

```json
{
  "duration": 20,
  "scenes": [
    {"type": "text", "duration": 3.5, "kicker": "FLEXI-CAP FUNDS",
     "lines": ["What even is", "a flexi-cap?"]},
    {"type": "bars", "duration": 4.5, "heading": "Where the money can go",
     "bars": [{"label": "Large-cap", "value": 0.4},
              {"label": "Mid-cap", "value": 0.35},
              {"label": "Small-cap", "value": 0.25}]},
    {"type": "circle", "duration": 4.0, "heading": "No fixed split",
     "label": "The fund manager decides the mix, and can change it"},
    {"type": "text", "duration": 4.0, "lines": ["That flexibility", "is the whole point"]}
  ]
}
```

Three scene `type`s are built in: `text` (kicker + kinetic lines), `bars`
(labeled bar chart), `circle` (animated donut ring). Extend
`scene_body_html()` / `build_scenes()` in `assemble.py` for hand-drawn SVG
diagram scenes as a project needs them.

## Compliance note

`bars` scenes auto-stamp `ILLUSTRATIVE ONLY` under the chart unless a scene
supplies its own `note`. **Never** put a real invented return figure in a
`bars` or `circle` value — these are for illustrating a *structure*
(allocation splits, a process), not performance (PLAYBOOK.md §2).

## Crossfades

Scenes cross-dissolve into each other (`CROSSFADE = 0.4s` in
`assemble.py`). Adjacent scenes are placed on alternating
`data-track-index` values (2 / 3) specifically so their overlapping visible
windows don't collide with HyperFrames' "overlapping clips on the same
track" lint error (PLAYBOOK.md §9.5).

## Editing loop

```bash
python3 assemble.py
npx hyperframes lint public
npx hyperframes snapshot public --at 2,8,15,22
PRODUCER_BROWSER_GPU_MODE=hardware \
  npx hyperframes render public --skill=faceless-explainer -o output.mp4 --fps 30
```
