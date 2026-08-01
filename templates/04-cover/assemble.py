#!/usr/bin/env python3
"""
Assembler for Archetype 4 — still Reels cover / thumbnail (PLAYBOOK.md §4,
skill `/motion-graphics`, rendered as a single-frame snapshot, not an MP4).

Reads an optional `config.json`; falls back to demo content so
`python3 assemble.py` renders on its own (against a placeholder photo panel
if `photo.jpg` isn't present in the project folder).

  config.json:
  {
    "photo": "photo.jpg",
    "hook_lines": ["Why one fund", "isn't a plan"],
    "name": "Vedant", "role": "Prospur"
  }

Render as a snapshot, not a video:

  npx hyperframes lint public
  npx hyperframes snapshot public --at 0 -o cover.png

Instagram crops a cover three ways (§4): Reels player (full 1080x1920),
feed (a centered 4:5 slice, roughly y=285-1635), profile grid (a centered
1:1 slice, roughly y=420-1500). The hook headline is placed in the upper
band (~y=250-560) so it survives all three crops; nothing load-bearing goes
below y=1500 or it's grid-invisible.
"""
import json
import os

CANVAS_W = 1080
CANVAS_H = 1920
COMP_ID = "reel-cover"

BRAND = "#047857"
POP = "#34D399"
ARN = "ARN-348873"

HERE = os.path.dirname(os.path.abspath(__file__))

DEMO_CONFIG = {
    "photo": "photo.jpg",
    "hook_lines": ["Why one fund", "isn't a plan"],
    "name": "Vedant",
    "role": "Prospur",
}


def load_json(name, default):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def main():
    config = {**DEMO_CONFIG, **load_json("config.json", {})}
    photo = config["photo"]
    photo_exists = os.path.exists(os.path.join(HERE, photo))

    lines_html = "".join(f'<div class="hook-line">{t}</div>' for t in config["hook_lines"])

    photo_html = (
        f'<img id="photo" src="{photo}" class="photo" />'
        if photo_exists
        else '<div class="photo photo--placeholder"></div>'
    )

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>reel-cover</title>
<link rel="stylesheet" href="../../../assets/fonts/fonts.css" />
<style>
  html, body {{ margin: 0; padding: 0; background: #000; }}
  #stage {{
    position: relative; width: {CANVAS_W}px; height: {CANVAS_H}px;
    overflow: hidden; font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  }}

  .photo {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
  .photo--placeholder {{ background: linear-gradient(160deg, #0c1a15 0%, #16211c 60%, #0c1a15 100%); }}

  .photo-scrim {{
    position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.05) 42%, rgba(0,0,0,0.15) 78%, rgba(0,0,0,0.62) 100%);
  }}

  /* Ghost background element: an oversized, low-opacity brand mark behind the hook,
     purely decorative texture — never load-bearing text. */
  .ghost {{
    position: absolute; top: -120px; right: -180px; width: 820px; height: 820px;
    border-radius: 50%; border: 60px solid {POP}; opacity: 0.10;
  }}

  .hook {{
    position: absolute; left: 64px; right: 64px; top: 250px;
  }}
  .hook-line {{
    color: #fff; font-weight: 700; font-size: 86px; line-height: 1.08;
    text-shadow: 0 3px 22px rgba(0,0,0,0.5);
  }}

  .name-tag {{
    position: absolute; left: 64px; bottom: 210px;
    display: flex; align-items: center; gap: 14px;
  }}
  .name-tag-rule {{ width: 44px; height: 4px; background: {POP}; }}
  .name-tag-text {{ color: #fff; }}
  .name-tag-name {{ font-weight: 700; font-size: 30px; }}
  .name-tag-role {{ font-weight: 400; font-size: 20px; color: rgba(255,255,255,0.78); }}

  .arn-chip {{
    position: absolute; left: 64px; bottom: 150px;
    font-weight: 500; font-size: 17px; color: rgba(255,255,255,0.68);
  }}

  .brand-mark {{ position: absolute; top: 64px; right: 64px; width: 176px; }}
  .brand-mark img {{ width: 100%; height: auto; filter: brightness(0) invert(1); }}
</style>
</head>
<body>
<div id="stage" data-composition-id="{COMP_ID}" data-start="0" data-duration="1"
     data-fps="30" data-width="{CANVAS_W}" data-height="{CANVAS_H}">

  {photo_html}
  <div class="photo-scrim"></div>
  <div class="ghost"></div>

  <div class="hook">{lines_html}</div>

  <div class="name-tag">
    <div class="name-tag-rule"></div>
    <div class="name-tag-text">
      <div class="name-tag-name">{config["name"]}</div>
      <div class="name-tag-role">{config["role"]}</div>
    </div>
  </div>
  <div class="arn-chip">Prospur · AMFI-registered MFD · {ARN}</div>

  <div class="brand-mark"><img src="../../../assets/prospur-logo.png" alt="Prospur" /></div>
</div>
<script>
(function () {{
  // Snapshot comp: no motion needed, but HyperFrames still expects a single
  // paused timeline registered for the composition id (PLAYBOOK §9.10).
  var tl = gsap.timeline({{ paused: true }});
  tl.set('#stage', {{}}, 0);
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
    print(f"wrote {out_path} (photo {'found' if photo_exists else 'MISSING, using placeholder'}: {photo})")


if __name__ == "__main__":
    main()
