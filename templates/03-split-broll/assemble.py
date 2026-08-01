#!/usr/bin/env python3
"""
Assembler for Archetype 3 — split-screen B-roll (PLAYBOOK.md §4, §8, skill
`/general-video`).

The video itself (`public/input-video.mp4`) is pre-composited by
`build_clips.sh` — two halves already hstacked, music bed already muxed
(PLAYBOOK.md §8). This script only builds the kinetic overlay: divider
glow, paired label chips, a word-pop hook, an optional running counter, and
an optional jar-fill SVG — plus the mandatory compliance strip.

Reads an optional `config.json`; falls back to demo content (SAVER│SPENDER)
so `python3 assemble.py` renders on its own.

  config.json:
  {
    "duration": 25.5,
    "left_label": "SAVER", "right_label": "SPENDER",
    "hook_lines": ["Same income.", "Different habits."],
    "counter": {"enabled": true, "target": 37, "label": "days of consistency", "note": "ILLUSTRATIVE ONLY"},
    "jar": {"enabled": true, "fill_pct": 0.7}
  }

Counter/jar values are illustrative UI motifs, not fund performance — keep
them labeled ILLUSTRATIVE ONLY and never let them imply a real return figure
(PLAYBOOK.md §2).
"""
import json
import os

FPS = 30
CANVAS_W = 1080
CANVAS_H = 1920
COMP_ID = "split-broll"

BRAND = "#047857"
POP = "#34D399"
SPEND = "#F59E0B"

COMPLIANCE_LINES = [
    "Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873",
    "Mutual funds are subject to market risks. Read all scheme-related documents carefully.",
    "For information only, not investment advice.",
]

HERE = os.path.dirname(os.path.abspath(__file__))

DEMO_CONFIG = {
    "duration": 25.5,
    "left_label": "SAVER",
    "right_label": "SPENDER",
    "hook_lines": ["Same income.", "Different habits."],
    "counter": {"enabled": True, "target": 37, "label": "days of consistency", "note": "ILLUSTRATIVE ONLY"},
    "jar": {"enabled": True, "fill_pct": 0.7},
}


def q(t):
    return round(round(t * FPS) / FPS, 3)


def load_json(name, default):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def divider_html(duration):
    return f'''
  <div id="divider" class="clip" data-track-index="1" data-start="0" data-duration="{duration}">
    <div class="divider-inner"></div>
  </div>'''


def label_chips_html(left_label, right_label, duration):
    return f'''
  <div id="label-left" class="clip" data-track-index="2" data-start="0" data-duration="{duration}">
    <div class="label-chip label-chip--left">{left_label}</div>
  </div>
  <div id="label-right" class="clip" data-track-index="3" data-start="0" data-duration="{duration}">
    <div class="label-chip label-chip--right">{right_label}</div>
  </div>'''


def hook_html(hook_lines, start, end):
    dur = q(end - start)
    lines_html = "".join(
        "".join(f'<span class="hook-word">{w}</span> ' for w in line.split()) + '<br/>'
        for line in hook_lines
    )
    return f'''
  <div id="hook" class="clip" data-track-index="4" data-start="{start}" data-duration="{dur}">
    <div class="hook-scrim"></div>
    <div class="hook-inner">{lines_html}</div>
  </div>'''


def counter_html(counter, duration):
    if not counter or not counter.get("enabled"):
        return ""
    return f'''
  <div id="counter" class="clip" data-track-index="5" data-start="0.6" data-duration="{q(duration - 0.6)}">
    <div class="counter-inner">
      <div class="counter-value" id="counter-value">0</div>
      <div class="counter-label">{counter["label"]}</div>
      <div class="counter-note">{counter.get("note", "ILLUSTRATIVE ONLY")}</div>
    </div>
  </div>'''


def jar_html(jar, duration):
    if not jar or not jar.get("enabled"):
        return ""
    return f'''
  <div id="jar" class="clip" data-track-index="6" data-start="0.6" data-duration="{q(duration - 0.6)}">
    <div class="jar-inner">
      <svg viewBox="0 0 120 160" class="jar-svg">
        <clipPath id="jar-clip"><rect x="14" y="30" width="92" height="120" rx="10"/></clipPath>
        <rect class="jar-fill-rect" x="14" y="150" width="92" height="120" rx="10" clip-path="url(#jar-clip)"/>
        <rect x="14" y="30" width="92" height="120" rx="10" fill="none" stroke="{BRAND}" stroke-width="4"/>
        <rect x="42" y="14" width="36" height="18" rx="4" fill="none" stroke="{BRAND}" stroke-width="4"/>
      </svg>
      <div class="jar-note">illustrative</div>
    </div>
  </div>'''


def brand_mark_html(duration):
    return f"""
  <div id="brand-mark" class="clip" data-track-index="7" data-start="0" data-duration="{duration}">
    <div class="brand-mark-inner">
      <img src="../../../assets/prospur-logo.png" alt="Prospur" class="brand-mark-img" />
    </div>
  </div>"""


def compliance_strip_html(duration):
    lines_html = "".join(
        f'<div class="compliance-line compliance-line--{i}">{txt}</div>'
        for i, txt in enumerate(COMPLIANCE_LINES)
    )
    return f"""
  <div id="compliance" class="clip" data-track-index="8" data-start="0" data-duration="{duration}">
    <div class="compliance-inner">
      <div class="compliance-scrim"></div>
      <div class="compliance-text">{lines_html}</div>
    </div>
  </div>"""


def build_timeline_js(hook_start, hook_end, has_counter, counter_target, has_jar, jar_fill_pct):
    stmts = []
    stmts.append(
        "tl.fromTo('.divider-inner', { opacity: 0, scaleY: 0 }, "
        "{ opacity: 1, scaleY: 1, duration: 0.5, ease: 'power2.out', transformOrigin: 'center center' }, 0.1);"
    )
    stmts.append(
        "tl.fromTo('.label-chip--left', { opacity: 0, x: -20 }, "
        "{ opacity: 1, x: 0, duration: 0.35, ease: 'power2.out' }, 0.3);"
    )
    stmts.append(
        "tl.fromTo('.label-chip--right', { opacity: 0, x: 20 }, "
        "{ opacity: 1, x: 0, duration: 0.35, ease: 'power2.out' }, 0.3);"
    )

    stmts.append(
        f"tl.fromTo('#hook .hook-scrim', {{ opacity: 0 }}, "
        f"{{ opacity: 1, duration: 0.25, ease: 'power1.out' }}, {hook_start});"
    )
    stmts.append(
        f"tl.fromTo('#hook .hook-word', {{ opacity: 0, y: 18, scale: 0.9 }}, "
        f"{{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: 'back.out(1.6)', stagger: 0.06 }}, "
        f"{q(hook_start + 0.1)});"
    )
    stmts.append(
        f"tl.to('#hook .hook-scrim, #hook .hook-inner', {{ opacity: 0, duration: 0.3, ease: 'power2.in' }}, "
        f"{q(hook_end - 0.3)});"
    )
    stmts.append(f"tl.set('#hook .hook-scrim, #hook .hook-inner', {{ opacity: 0, visibility: 'hidden' }}, {hook_end});")

    if has_counter:
        stmts.append(
            "tl.fromTo('.counter-inner', { opacity: 0, y: 12 }, "
            "{ opacity: 1, y: 0, duration: 0.35, ease: 'power2.out' }, 1.0);"
        )
        stmts.append(
            "(function(){ var c = { v: 0 }; "
            f"tl.to(c, {{ v: {counter_target}, duration: 1.4, ease: 'power1.out', "
            "onUpdate: function () { document.getElementById('counter-value').textContent = Math.round(c.v); } "
            "}, 1.2); })();"
        )
    if has_jar:
        stmts.append(
            "tl.fromTo('.jar-inner', { opacity: 0 }, "
            "{ opacity: 1, duration: 0.35, ease: 'power2.out' }, 1.0);"
        )
        stmts.append(
            f"tl.to('.jar-fill-rect', {{ y: {q(150 - 120 * jar_fill_pct)}, duration: 1.6, ease: 'power2.inOut' }}, 1.3);"
        )

    stmts.append(
        "tl.fromTo('.brand-mark-inner', { opacity: 0 }, "
        "{ opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.15);"
    )
    stmts.append(
        "tl.fromTo('.compliance-inner', { opacity: 0 }, "
        "{ opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.15);"
    )
    return "\n  ".join(stmts)


def main():
    config = {**DEMO_CONFIG, **load_json("config.json", {})}
    duration = config["duration"]
    hook_start, hook_end = 0.3, min(3.2, duration)

    counter = config.get("counter")
    jar = config.get("jar")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>split-broll</title>
<link rel="stylesheet" href="../../../assets/fonts/fonts.css" />
<style>
  html, body {{ margin: 0; padding: 0; background: #000; }}
  #stage {{
    position: relative; width: {CANVAS_W}px; height: {CANVAS_H}px;
    overflow: hidden; font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  }}
  video#input-video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}

  .divider-inner {{
    position: absolute; top: 0; left: 537px; width: 6px; height: 100%;
    background: #fff; box-shadow: 0 0 24px 4px {BRAND}; opacity: 0;
  }}

  .label-chip {{
    position: absolute; top: 96px; padding: 10px 22px; border-radius: 999px;
    font-weight: 700; font-size: 26px; letter-spacing: 0.05em; color: #fff; opacity: 0;
  }}
  .label-chip--left {{ left: 40px; background: {BRAND}; }}
  .label-chip--right {{ right: 40px; background: {SPEND}; }}

  .hook-scrim {{
    position: absolute; inset: 0; background: rgba(0,0,0,0.38); opacity: 0;
  }}
  .hook-inner {{
    position: absolute; left: 64px; right: 64px; top: 760px; text-align: center;
  }}
  .hook-word {{
    display: inline-block; margin: 0 0.16em; color: #fff; font-weight: 700; font-size: 66px;
    text-shadow: 0 2px 16px rgba(0,0,0,0.5); opacity: 0;
  }}

  .counter-inner {{
    position: absolute; left: 0; right: 0; top: 1180px; text-align: center; opacity: 0;
  }}
  .counter-value {{ color: #fff; font-weight: 700; font-size: 88px; text-shadow: 0 2px 14px rgba(0,0,0,0.55); }}
  .counter-label {{ color: rgba(255,255,255,0.9); font-weight: 400; font-size: 24px; margin-top: 4px; }}
  .counter-note {{
    color: rgba(255,255,255,0.65); font-weight: 700; font-size: 15px; letter-spacing: 0.08em; margin-top: 8px;
  }}

  .jar-inner {{
    position: absolute; left: 0; right: 0; top: 1300px; display: flex; flex-direction: column;
    align-items: center; opacity: 0;
  }}
  .jar-svg {{ width: 130px; height: auto; }}
  .jar-fill-rect {{ fill: {POP}; }}
  .jar-note {{
    color: rgba(255,255,255,0.65); font-weight: 700; font-size: 14px; letter-spacing: 0.08em; margin-top: 6px;
  }}

  .brand-mark-inner {{ position: absolute; top: 56px; right: 56px; width: 176px; opacity: 0; }}
  .brand-mark-img {{ width: 100%; height: auto; filter: brightness(0) invert(1); }}

  .compliance-inner {{ position: absolute; left: 0; right: 0; bottom: 44px; opacity: 0; }}
  .compliance-scrim {{
    position: absolute; left: 0; right: 0; bottom: 0; height: 220px;
    background: linear-gradient(0deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0) 100%);
  }}
  .compliance-text {{
    position: relative; padding: 0 48px 26px; color: rgba(255,255,255,0.86);
    text-shadow: 0 1px 6px rgba(0,0,0,0.6);
  }}
  .compliance-line {{ font-weight: 500; font-size: 19px; line-height: 1.4; }}
</style>
</head>
<body>
<div id="stage" data-composition-id="{COMP_ID}" data-start="0" data-duration="{duration}"
     data-fps="{FPS}" data-width="{CANVAS_W}" data-height="{CANVAS_H}">

  <video id="input-video" class="clip" data-track-index="0" data-start="0" data-duration="{duration}"
         src="input-video.mp4" muted playsinline></video>
{divider_html(duration)}
{label_chips_html(config["left_label"], config["right_label"], duration)}
{hook_html(config["hook_lines"], hook_start, hook_end)}
{counter_html(counter, duration)}
{jar_html(jar, duration)}
{brand_mark_html(duration)}
{compliance_strip_html(duration)}

  <audio id="music-track" class="clip" data-track-index="10" data-start="0" data-duration="{duration}"
         src="input-video.mp4"></audio>
</div>
<script>
(function () {{
  var tl = gsap.timeline({{ paused: true }});
  {build_timeline_js(
      hook_start, hook_end,
      bool(counter and counter.get("enabled")), (counter or {}).get("target", 0),
      bool(jar and jar.get("enabled")), (jar or {}).get("fill_pct", 0.5),
  )}
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
    print(f"wrote {out_path} ({duration}s)")


if __name__ == "__main__":
    main()
