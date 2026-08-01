#!/usr/bin/env python3
"""
Assembler for Archetype 2 — faceless explainer (PLAYBOOK.md §4, skill
`/faceless-explainer`).

No footage: pure editorial serif type + kinetic graphics on a warm-paper
background, scenes joined with cross-dissolve. Reads an optional
`config.json` with a `scenes` array; falls back to a demo script so
`python3 assemble.py` always renders on its own.

  config.json:
  {
    "duration": 20,
    "scenes": [
      {"type": "text", "duration": 3.5, "kicker": "...", "lines": ["...", "..."]},
      {"type": "bars", "duration": 4.5, "heading": "...", "note": "ILLUSTRATIVE ONLY",
       "bars": [{"label": "...", "value": 0.4}, ...]},
      {"type": "circle", "duration": 4, "heading": "...", "label": "..."},
      ...
    ]
  }

Every numeric graphic must either be the speaker's own words (n/a here —
there's no speaker) or be masked / labeled ILLUSTRATIVE ONLY — never a real
invented return figure (PLAYBOOK.md §2). `bars` and `circle` scenes without
an explicit `note` get "ILLUSTRATIVE ONLY" stamped automatically.
"""
import json
import os

FPS = 30
CANVAS_W = 1080
CANVAS_H = 1920
COMP_ID = "faceless-explainer"
CROSSFADE = 0.4  # seconds of overlap between adjacent scenes

BRAND = "#047857"
POP = "#34D399"
TEXT_DARK = "#16211C"
PAPER = "#F3EDE1"

COMPLIANCE_LINES = [
    "Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873",
    "Mutual funds are subject to market risks. Read all scheme-related documents carefully.",
    "For information only, not investment advice.",
]

HERE = os.path.dirname(os.path.abspath(__file__))

DEMO_SCENES = [
    {"type": "text", "duration": 3.5, "kicker": "FLEXI-CAP FUNDS",
     "lines": ["What even is", "a flexi-cap?"]},
    {"type": "bars", "duration": 4.5, "heading": "Where the money can go",
     "bars": [{"label": "Large-cap", "value": 0.4},
              {"label": "Mid-cap", "value": 0.35},
              {"label": "Small-cap", "value": 0.25}]},
    {"type": "circle", "duration": 4.0, "heading": "No fixed split",
     "label": "The fund manager decides the mix, and can change it"},
    {"type": "text", "duration": 4.0,
     "lines": ["That flexibility", "is the whole point"]},
]


def q(t):
    return round(round(t * FPS) / FPS, 3)


def load_json(name, default):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def scene_body_html(scene, idx):
    stype = scene["type"]
    if stype == "text":
        kicker = f'<div class="scene-kicker">{scene["kicker"]}</div>' if scene.get("kicker") else ""
        lines = "".join(f'<div class="scene-line">{t}</div>' for t in scene["lines"])
        return f'<div class="scene-text">{kicker}{lines}</div>'
    if stype == "bars":
        note = scene.get("note", "ILLUSTRATIVE ONLY")
        bars = "".join(
            f'''<div class="bar-row">
                  <div class="bar-label">{b["label"]}</div>
                  <div class="bar-track"><div class="bar-fill" data-scene="{idx}" data-value="{b["value"]}"></div></div>
                </div>'''
            for b in scene["bars"]
        )
        return f'''<div class="scene-chart">
          <div class="scene-heading">{scene["heading"]}</div>
          {bars}
          <div class="scene-note">{note}</div>
        </div>'''
    if stype == "circle":
        return f'''<div class="scene-circle">
          <div class="scene-heading">{scene["heading"]}</div>
          <svg viewBox="0 0 200 200" class="donut" data-scene="{idx}">
            <circle cx="100" cy="100" r="86" fill="none" stroke="{TEXT_DARK}" stroke-opacity="0.12" stroke-width="14"/>
            <circle class="donut-ring" cx="100" cy="100" r="86" fill="none" stroke="{BRAND}" stroke-width="14"
                    stroke-linecap="round" stroke-dasharray="540" stroke-dashoffset="540"
                    transform="rotate(-90 100 100)"/>
          </svg>
          <div class="scene-caption">{scene["label"]}</div>
        </div>'''
    raise ValueError(f"unknown scene type: {stype}")


def build_scenes(scenes):
    """Returns (html, timeline_stmts, total_duration)."""
    html_parts, stmts = [], []
    t = 0.0
    for idx, scene in enumerate(scenes):
        dur = scene["duration"]
        track = 2 + (idx % 2)  # alternate tracks so crossfades can overlap (§9.5)
        start = q(max(0, t - (CROSSFADE if idx > 0 else 0)))
        span = q(dur + (CROSSFADE if idx > 0 else 0) + (CROSSFADE if idx < len(scenes) - 1 else 0))
        cid = f"scene-{idx}"

        html_parts.append(f'''
  <div id="{cid}" class="clip" data-track-index="{track}" data-start="{start}" data-duration="{span}">
    <div class="scene-inner">{scene_body_html(scene, idx)}</div>
  </div>''')

        fade_in_at = start if idx == 0 else q(start + CROSSFADE - CROSSFADE)  # element becomes visible at its own start
        stmts.append(
            f"tl.fromTo('#{cid} .scene-inner', {{ opacity: 0 }}, "
            f"{{ opacity: 1, duration: {CROSSFADE}, ease: 'power1.inOut' }}, {start});"
        )
        exit_at = q(start + span - CROSSFADE)
        stmts.append(
            f"tl.to('#{cid} .scene-inner', {{ opacity: 0, duration: {CROSSFADE}, ease: 'power1.inOut' }}, {exit_at});"
        )
        stmts.append(f"tl.set('#{cid} .scene-inner', {{ opacity: 0, visibility: 'hidden' }}, {q(start + span)});")

        # kinetic content per scene type
        if scene["type"] == "text":
            stmts.append(
                f"tl.fromTo('#{cid} .scene-line', {{ opacity: 0, y: 20 }}, "
                f"{{ opacity: 1, y: 0, duration: 0.45, ease: 'power2.out', stagger: 0.1 }}, {q(start + CROSSFADE)});"
            )
        elif scene["type"] == "bars":
            stmts.append(
                f"tl.fromTo('#{cid} .bar-fill', {{ scaleX: 0 }}, "
                f"{{ scaleX: 1, duration: 0.6, ease: 'power2.out', stagger: 0.12, "
                f"transformOrigin: 'left center' }}, {q(start + CROSSFADE + 0.1)});"
            )
        elif scene["type"] == "circle":
            stmts.append(
                f"tl.to('#{cid} .donut-ring', {{ strokeDashoffset: 90, duration: 0.9, ease: 'power2.inOut' }}, "
                f"{q(start + CROSSFADE + 0.1)});"
            )

        t = t + dur
    return "".join(html_parts), stmts, q(t)


def compliance_strip_html(duration):
    lines_html = "".join(
        f'<div class="compliance-line compliance-line--{i}">{txt}</div>'
        for i, txt in enumerate(COMPLIANCE_LINES)
    )
    return f"""
  <div id="compliance" class="clip" data-track-index="8" data-start="0" data-duration="{duration}">
    <div class="compliance-inner">
      <div class="compliance-text">{lines_html}</div>
    </div>
  </div>"""


def brand_mark_html(duration):
    return f"""
  <div id="brand-mark" class="clip" data-track-index="7" data-start="0" data-duration="{duration}">
    <div class="brand-mark-inner">
      <img src="../../../assets/prospur-logo.png" alt="Prospur" class="brand-mark-img" />
    </div>
  </div>"""


def main():
    config = load_json("config.json", {})
    scenes = config.get("scenes", DEMO_SCENES)

    scenes_html, scene_stmts, duration = build_scenes(scenes)

    compliance_stmt = (
        "tl.fromTo('.compliance-inner', { opacity: 0 }, "
        "{ opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.15);"
    )
    brand_stmt = (
        "tl.fromTo('.brand-mark-inner', { opacity: 0 }, "
        "{ opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.15);"
    )
    timeline_js = "\n  ".join(scene_stmts + [compliance_stmt, brand_stmt])

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>faceless-explainer</title>
<link rel="stylesheet" href="../../../assets/fonts/fonts.css" />
<style>
  html, body {{ margin: 0; padding: 0; background: {PAPER}; }}
  #stage {{
    position: relative; width: {CANVAS_W}px; height: {CANVAS_H}px;
    overflow: hidden; background: {PAPER};
    font-family: 'Source Serif 4', Georgia, serif;
  }}
  .scene-inner {{
    position: absolute; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; padding: 0 96px; opacity: 0;
  }}

  .scene-kicker {{
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; font-weight: 700;
    font-size: 24px; letter-spacing: 0.08em; color: {BRAND}; margin-bottom: 28px;
  }}
  .scene-line {{
    font-weight: 600; font-size: 72px; line-height: 1.16; color: {TEXT_DARK};
    text-align: center;
  }}

  .scene-chart {{ width: 100%; }}
  .scene-heading {{
    font-weight: 600; font-size: 48px; color: {TEXT_DARK}; margin-bottom: 56px; text-align: center;
  }}
  .bar-row {{ display: flex; align-items: center; margin-bottom: 34px; }}
  .bar-label {{
    font-family: 'Inter', sans-serif; font-weight: 400; font-size: 26px; color: {TEXT_DARK};
    width: 220px; flex-shrink: 0;
  }}
  .bar-track {{ flex: 1; height: 28px; background: rgba(22,33,28,0.08); border-radius: 6px; overflow: hidden; }}
  .bar-fill {{ height: 100%; background: {BRAND}; border-radius: 6px; transform: scaleX(0); }}
  .scene-note {{
    font-family: 'Inter', sans-serif; font-weight: 700; font-size: 20px; letter-spacing: 0.06em;
    color: {TEXT_DARK}; opacity: 0.55; text-align: center; margin-top: 36px;
  }}

  .scene-circle {{ display: flex; flex-direction: column; align-items: center; }}
  .donut {{ width: 320px; height: 320px; margin: 20px 0 40px; }}
  .scene-caption {{
    font-family: 'Inter', sans-serif; font-weight: 400; font-size: 26px; color: {TEXT_DARK};
    text-align: center; max-width: 640px; line-height: 1.4;
  }}

  .brand-mark-inner {{ position: absolute; top: 56px; right: 56px; width: 176px; opacity: 0; }}
  .brand-mark-img {{ width: 100%; height: auto; }}

  .compliance-inner {{
    position: absolute; left: 0; right: 0; bottom: 44px; opacity: 0;
  }}
  .compliance-text {{
    padding: 0 48px; color: {TEXT_DARK}; font-family: 'Inter', sans-serif;
  }}
  .compliance-line {{ font-weight: 500; font-size: 19px; line-height: 1.4; opacity: 0.72; }}
</style>
</head>
<body>
<div id="stage" data-composition-id="{COMP_ID}" data-start="0" data-duration="{duration}"
     data-fps="{FPS}" data-width="{CANVAS_W}" data-height="{CANVAS_H}">
{scenes_html}
{brand_mark_html(duration)}
{compliance_strip_html(duration)}
</div>
<script>
(function () {{
  var tl = gsap.timeline({{ paused: true }});
  {timeline_js}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{COMP_ID}"] = tl;
}})();
</script>
</body>
</html>
"""

    out_dir = os.path.join(HERE, "public")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"wrote {out_path} ({duration}s, {len(scenes)} scenes)")


if __name__ == "__main__":
    main()
