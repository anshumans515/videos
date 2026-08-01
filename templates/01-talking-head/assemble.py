#!/usr/bin/env python3
"""
Assembler for Archetype 1 — talking-head recut (PLAYBOOK.md §4, skill
`/talking-head-recut`).

Reads (all optional — falls back to demo content so `python3 assemble.py`
always produces a renderable comp out of the box):

  config.json       { "duration": 24, "kicker": "...", "title_lines": [...],
                       "name": "...", "role": "...", "head_position": "standing" }
  transcript.json    [{ "word": "...", "start": 0.12, "end": 0.31 }, ...]
                      (Whisper word-level output — repair audio and
                      transcribe BEFORE trusting this file; see PLAYBOOK §3)

Writes public/index.html. Then run the standard loop (PLAYBOOK §10):

  npx hyperframes lint public
  npx hyperframes snapshot public --at 2,8,15,22
  PRODUCER_BROWSER_GPU_MODE=hardware \\
    npx hyperframes render public --skill=talking-head-recut -o output.mp4 --fps 30
"""
import json
import os

FPS = 30
CANVAS_W = 1080
CANVAS_H = 1920
COMP_ID = "talking-head-recut"

# ---- Brand tokens (PLAYBOOK.md §1) -----------------------------------------
BRAND = "#047857"
POP = "#34D399"
SPEND = "#F59E0B"
SPEND_HOT = "#F87171"
TEXT_DARK = "#16211C"
PAPER = "#F3EDE1"
ARN = "ARN-348873"

COMPLIANCE_LINES = [
    "Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873",
    "Mutual funds are subject to market risks. Read all scheme-related documents carefully.",
    "For information only, not investment advice.",
]

# Whisper's word-start timestamps run ~0.3s early (PLAYBOOK.md §6).
CAP_OFFSET = 0.34

HEAD_POSITION_SCRIM = {
    # head_position -> (card safe-height, scrim gradient height)
    "standing": (640, 760),
    "seated": (1020, 1040),
}

HERE = os.path.dirname(os.path.abspath(__file__))

DEMO_CONFIG = {
    "duration": 24,
    "head_position": "standing",
    "kicker": "MUTUAL FUNDS, EXPLAINED",
    "title_lines": ["Why one fund", "isn't a plan"],
    "name": "Vedant",
    "role": "Prospur",
}

DEMO_TRANSCRIPT = [
    {"word": w, "start": s, "end": s + 0.30}
    for w, s in zip(
        "A lot of people think one good fund is the whole plan but "
        "spreading it out is what actually protects you".split(),
        [round(2.0 + 0.34 * i, 2) for i in range(19)],
    )
]


def q(t):
    """Quantize a timestamp to the nearest frame."""
    return round(round(t * FPS) / FPS, 3)


def load_json(name, default):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def chunk_transcript(words, max_words=5, gap_break=0.6):
    """Group words into caption lines: PLAYBOOK §6 word-pop karaoke lines."""
    lines, current = [], []
    for w in words:
        if current and (
            len(current) >= max_words or w["start"] - current[-1]["end"] > gap_break
        ):
            lines.append(current)
            current = []
        current.append(w)
    if current:
        lines.append(current)
    return lines


# ---- Markup builders --------------------------------------------------------

def compliance_strip_html(duration):
    lines_html = "".join(
        f'<div class="compliance-line compliance-line--{i}">{t}</div>'
        for i, t in enumerate(COMPLIANCE_LINES)
    )
    return f"""
  <div id="compliance" class="clip" data-track-index="8" data-start="0" data-duration="{duration}">
    <div class="compliance-inner">
      <div class="compliance-scrim"></div>
      <div class="compliance-text">{lines_html}</div>
    </div>
  </div>"""


def scrim_html(duration, scrim_height):
    return f"""
  <div id="scrim" class="clip" data-track-index="1" data-start="0" data-duration="{duration}">
    <div class="scrim-inner" style="height:{scrim_height}px;"></div>
  </div>"""


def brand_mark_html(duration):
    return f"""
  <div id="brand-mark" class="clip" data-track-index="7" data-start="0" data-duration="{duration}">
    <div class="brand-mark-inner">
      <img src="../../../assets/prospur-logo.png" alt="Prospur" class="brand-mark-img" />
    </div>
  </div>"""


def kicker_title_html(kicker, title_lines, start, end):
    dur = q(end - start)
    title_html = "".join(f'<div class="title-line">{t}</div>' for t in title_lines)
    return f"""
  <div id="kicker" class="clip" data-track-index="2" data-start="{start}" data-duration="{dur}">
    <div class="kicker-inner"><span class="kicker-chip">{kicker}</span></div>
  </div>
  <div id="kinetic-title" class="clip" data-track-index="3" data-start="{start}" data-duration="{dur}">
    <div class="kinetic-title-inner">{title_html}</div>
  </div>"""


def lower_third_html(name, role, start, end):
    dur = q(end - start)
    return f"""
  <div id="lower-third" class="clip" data-track-index="4" data-start="{start}" data-duration="{dur}">
    <div class="lower-third-inner">
      <div class="lower-third-rule"></div>
      <div class="lower-third-name">{name}</div>
      <div class="lower-third-role">{role}</div>
    </div>
  </div>"""


def caption_line_html(cid, words):
    spans = "".join(f'<span id="{cid}-w{wi}" class="w">{w["word"]}</span> ' for wi, w in enumerate(words))
    start = q(words[0]["start"] + CAP_OFFSET)
    end = q(words[-1]["end"] + CAP_OFFSET)
    dur = q(end - start)
    return (
        f"""
  <div id="{cid}" class="clip" data-track-index="6" data-start="{start}" data-duration="{dur}">
    <div class="caption-inner">{spans}</div>
  </div>""",
        start,
        end,
    )


# ---- Timeline (GSAP) --------------------------------------------------------

def build_timeline_js(kicker_start, kicker_end, lt_start, lt_end, caption_lines):
    stmts = []

    # kicker + kinetic title: slide/fade in, hold, fade out on inner wrappers
    # (never animate opacity/visibility on the .clip element itself — §9.2)
    stmts.append(
        f"tl.fromTo('.kicker-inner', {{ opacity: 0, y: 16 }}, "
        f"{{ opacity: 1, y: 0, duration: 0.35, ease: 'power2.out' }}, {kicker_start});"
    )
    stmts.append(
        f"tl.fromTo('.kinetic-title-inner .title-line', {{ opacity: 0, y: 24 }}, "
        f"{{ opacity: 1, y: 0, duration: 0.4, ease: 'power2.out', stagger: 0.08 }}, {q(kicker_start + 0.08)});"
    )
    stmts.append(
        f"tl.to('.kicker-inner', {{ opacity: 0, duration: 0.2, ease: 'power2.in' }}, {q(kicker_end - 0.2)});"
    )
    stmts.append(f"tl.set('.kicker-inner', {{ opacity: 0 }}, {kicker_end});")
    stmts.append(
        f"tl.to('.kinetic-title-inner', {{ opacity: 0, duration: 0.2, ease: 'power2.in' }}, {q(kicker_end - 0.2)});"
    )
    stmts.append(f"tl.set('.kinetic-title-inner', {{ opacity: 0 }}, {kicker_end});")

    # lower third
    stmts.append(
        f"tl.fromTo('.lower-third-inner', {{ opacity: 0, x: -24 }}, "
        f"{{ opacity: 1, x: 0, duration: 0.35, ease: 'power2.out' }}, {lt_start});"
    )
    stmts.append(
        f"tl.to('.lower-third-inner', {{ opacity: 0, duration: 0.2, ease: 'power2.in' }}, {q(lt_end - 0.2)});"
    )
    stmts.append(f"tl.set('.lower-third-inner', {{ opacity: 0 }}, {lt_end});")

    # brand mark + compliance strip: fade in once, hold for the whole comp
    stmts.append(
        "tl.fromTo('.brand-mark-inner', { opacity: 0 }, "
        "{ opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.15);"
    )
    stmts.append(
        "tl.fromTo('.compliance-inner', { opacity: 0 }, "
        "{ opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.15);"
    )

    # karaoke captions
    for cid, words, start, end in caption_lines:
        n_words = len(words)
        span = end - start
        stmts.append(
            f"tl.fromTo('#{cid} .caption-inner', {{ opacity: 0, y: 10 }}, "
            f"{{ opacity: 1, y: 0, duration: 0.12, ease: 'power2.out' }}, {start});"
        )
        for wi in range(n_words):
            t = q(start + 0.04 + span * wi / max(n_words, 1))
            stmts.append(
                f"tl.to('#{cid}-w{wi}', {{ color: '{POP}', scale: 1.12, duration: 0.10, "
                f"ease: 'power2.out', overwrite: 'auto' }}, {t});"
            )
            stmts.append(
                f"tl.to('#{cid}-w{wi}', {{ scale: 1.0, duration: 0.13, ease: 'power2.in', "
                f"overwrite: 'auto' }}, {q(t + 0.11)});"
            )
        stmts.append(
            f"tl.to('#{cid} .caption-inner', {{ opacity: 0, duration: 0.12, ease: 'power2.in' }}, {q(end - 0.12)});"
        )
        stmts.append(f"tl.set('#{cid} .caption-inner', {{ opacity: 0, visibility: 'hidden' }}, {end});")

    return "\n  ".join(stmts)


# ---- Assemble ----------------------------------------------------------------

def main():
    config = {**DEMO_CONFIG, **load_json("config.json", {})}
    words = load_json("transcript.json", DEMO_TRANSCRIPT)

    duration = config["duration"]
    head_position = config.get("head_position", "standing")
    card_safe_h, scrim_h = HEAD_POSITION_SCRIM.get(head_position, HEAD_POSITION_SCRIM["standing"])

    kicker_start, kicker_end = 0.3, min(4.0, duration)
    lt_start, lt_end = 1.0, min(5.5, duration)

    caption_lines = []
    for i, line_words in enumerate(chunk_transcript(words)):
        cid = f"cap-{i}"
        html, start, end = caption_line_html(cid, line_words)
        caption_lines.append((cid, line_words, start, end))

    captions_html = "".join(caption_line_html(f"cap-{i}", lw)[0] for i, lw in enumerate(chunk_transcript(words)))
    timeline_js = build_timeline_js(kicker_start, kicker_end, lt_start, lt_end, caption_lines)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>talking-head-recut</title>
<link rel="stylesheet" href="../../../assets/fonts/fonts.css" />
<style>
  html, body {{ margin: 0; padding: 0; background: #000; }}
  #stage {{
    position: relative; width: {CANVAS_W}px; height: {CANVAS_H}px;
    overflow: hidden; font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  }}
  video#input-video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}

  .scrim-inner {{
    position: absolute; top: 0; left: 0; width: 100%;
    background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.32) 45%, rgba(0,0,0,0) 100%);
  }}

  .kicker-inner {{ position: absolute; top: 120px; left: 64px; opacity: 0; }}
  .kicker-chip {{
    display: inline-block; padding: 10px 20px; border-radius: 999px;
    background: {BRAND}; color: #fff; font-weight: 700; font-size: 24px;
    letter-spacing: 0.04em;
  }}

  .kinetic-title-inner {{
    position: absolute; top: 190px; left: 64px; right: 64px; opacity: 0;
  }}
  .title-line {{
    color: #fff; font-weight: 700; font-size: 76px; line-height: 1.06;
    text-shadow: 0 2px 18px rgba(0,0,0,0.45);
  }}

  .lower-third-inner {{
    position: absolute; left: 64px; top: {card_safe_h - 140}px; opacity: 0;
  }}
  .lower-third-rule {{ width: 56px; height: 4px; background: {POP}; margin-bottom: 10px; }}
  .lower-third-name {{ color: #fff; font-weight: 700; font-size: 34px; }}
  .lower-third-role {{ color: rgba(255,255,255,0.78); font-weight: 400; font-size: 22px; }}

  .caption-inner {{
    position: absolute; left: 64px; right: 64px; top: 1380px;
    font-weight: 700; font-size: 57px; line-height: 1.2; color: #fff;
    text-shadow: 0 2px 14px rgba(0,0,0,0.55);
  }}
  .caption-inner .w {{ margin: 0 0.19em; display: inline-block; }}

  .brand-mark-inner {{ position: absolute; top: 56px; right: 56px; width: 176px; opacity: 0; }}
  .brand-mark-img {{ width: 100%; height: auto; filter: brightness(0) invert(1); }}

  .compliance-inner {{
    position: absolute; left: 0; right: 0; bottom: 44px; opacity: 0;
  }}
  .compliance-scrim {{
    position: absolute; left: 0; right: 0; bottom: 0; height: 260px;
    background: linear-gradient(0deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0) 100%);
  }}
  .compliance-text {{
    position: relative; padding: 0 48px 28px; color: rgba(255,255,255,0.86);
    text-shadow: 0 1px 6px rgba(0,0,0,0.6);
  }}
  .compliance-line {{ font-weight: 500; font-size: 20px; line-height: 1.4; }}
</style>
</head>
<body>
<div id="stage" data-composition-id="{COMP_ID}" data-start="0" data-duration="{duration}"
     data-fps="{FPS}" data-width="{CANVAS_W}" data-height="{CANVAS_H}">

  <video id="input-video" class="clip" data-track-index="0" data-start="0" data-duration="{duration}"
         src="input-video.mp4" muted playsinline></video>
{scrim_html(duration, scrim_h)}
{kicker_title_html(config["kicker"], config["title_lines"], kicker_start, kicker_end)}
{lower_third_html(config["name"], config["role"], lt_start, lt_end)}
{captions_html}
{brand_mark_html(duration)}
{compliance_strip_html(duration)}

  <audio id="voice-track" class="clip" data-track-index="10" data-start="0" data-duration="{duration}"
         src="input-video.mp4"></audio>
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
    print(f"wrote {out_path} ({duration}s, {len(caption_lines)} caption lines)")


if __name__ == "__main__":
    main()
