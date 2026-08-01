#!/usr/bin/env python3
"""
Reels cover for the SAVER vs SPENDER reel — Archetype 4 (PLAYBOOK.md §4).
Rendered as a single-frame PNG snapshot, not an MP4.

  python3 assemble.py
  npx hyperframes lint public
  npx hyperframes snapshot public --at 0

WHY TWO CIRCLES RATHER THAN A SPLIT-SCREEN STILL
Instagram crops a cover three ways: the Reels player shows the full
1080x1920, the feed takes a centred 4:5 slice (~y285-1635), and the profile
grid takes a centred 1:1 slice (~y420-1500). A stacked split-screen still
loses its whole top half to the grid crop and reads as one random frame.
Two circular portraits sit inside the 1:1 band, so the comparison — the
entire point of the reel — survives every crop.
"""
import os

CANVAS_W, CANVAS_H = 1080, 1920
COMP_ID = "prospur-cover"

BRAND = "#047857"
POP = "#34D399"
SPEND = "#F59E0B"

# Broken by hand rather than left to wrap: at 96px "Different month-end."
# auto-wraps to "Different month-" / "end.", which reads as a typo at a glance.
HOOK_LINES = [
    ("Same salary.", "hook-line--white"),
    ("Different", "hook-line--pop"),
    ("month-end.", "hook-line--pop"),
]
ARN_LINE = "Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873"
CTA_CHIP = "DM us  ·  Start your SIP"

# circle geometry — both inside the ~y420-1500 profile-grid band
CIRCLE_D = 424
CIRCLE_Y = 700
LEFT_X, RIGHT_X = 74, 582

HERE = os.path.dirname(os.path.abspath(__file__))


def brand_lockup():
    """Real wordmark when present, typographic lockup otherwise. Drop the asset
    at public/img/prospur-logo.png and re-run to swap it in."""
    if os.path.exists(os.path.join(HERE, "public", "img", "prospur-logo.png")):
        return '<img src="img/prospur-logo.png" class="brand-img" alt="Prospur" />'
    return (
        f'<span class="wordmark">'
        f'<svg class="wordmark-mark" viewBox="0 0 40 40" aria-hidden="true">'
        f'<rect x="1.5" y="1.5" width="37" height="37" rx="11" fill="{BRAND}"/>'
        f'<path d="M11 26.5 L18 19 L23 24 L30.5 14.5" fill="none" stroke="#fff" '
        f'stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="30.5" cy="14.5" r="2.9" fill="{POP}"/></svg>'
        f'<span class="wordmark-text">Prospur</span></span>'
    )


def person(side, img, name, label, colour, x):
    return f"""
    <div class="person person--{side}" style="left:{x}px;">
      <div class="ring" style="border-color:{colour};">
        <img src="img/{img}" class="portrait" alt="{name}" />
      </div>
      <div class="person-name">{name}</div>
      <div class="person-label" style="color:{colour};">{label}</div>
    </div>"""


hook_html = "".join(f'<div class="hook-line {cls}">{t}</div>' for t, cls in HOOK_LINES)

HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Prospur — Saver vs Spender (cover)</title>
<style>
  @font-face {{ font-family: 'Inter'; src: url('fonts/Inter-Regular.woff2') format('woff2');
               font-weight: 400; font-style: normal; font-display: block; }}
  @font-face {{ font-family: 'Inter'; src: url('fonts/Inter-Bold.woff2') format('woff2');
               font-weight: 700; font-style: normal; font-display: block; }}

  html, body {{ margin: 0; padding: 0; background: #050B09; }}
  #stage {{ position: relative; width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden;
            font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
            background:
              radial-gradient(1100px 780px at 18% 6%, rgba(4,120,87,0.42) 0%, rgba(5,11,9,0) 62%),
              radial-gradient(900px 700px at 92% 96%, rgba(245,158,11,0.20) 0%, rgba(5,11,9,0) 60%),
              linear-gradient(168deg, #08150F 0%, #050B09 55%, #04100C 100%); }}

  /* ghost background element — decorative texture only, never load-bearing */
  .ghost {{ position: absolute; top: -230px; right: -280px; width: 900px; height: 900px;
            border-radius: 50%; border: 74px solid {POP}; opacity: 0.075; }}
  .ghost--2 {{ top: auto; bottom: -300px; left: -300px; right: auto; width: 760px; height: 760px;
               border: 62px solid {SPEND}; opacity: 0.06; }}

  .top-mark {{ position: absolute; top: 84px; left: 74px; }}

  /* hook lives in the upper band so it survives the 4:5 feed crop (~y285+) */
  .hook {{ position: absolute; top: 296px; left: 74px; width: 932px; }}
  .hook-line {{ font-weight: 700; font-size: 96px; line-height: 1.08; letter-spacing: -0.022em; }}
  .hook-line--white {{ color: #fff; }}
  .hook-line--pop {{ color: {POP}; }}

  .person {{ position: absolute; top: {CIRCLE_Y}px; width: {CIRCLE_D}px; text-align: center; }}
  .ring {{ width: {CIRCLE_D}px; height: {CIRCLE_D}px; border-radius: 50%; border: 9px solid;
           overflow: hidden; box-shadow: 0 22px 60px rgba(0,0,0,0.55); }}
  .portrait {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .person-name {{ margin-top: 26px; font-weight: 400; font-size: 25px; letter-spacing: 0.17em;
                  color: rgba(255,255,255,0.62); }}
  .person-label {{ margin-top: 8px; font-weight: 700; font-size: 42px; letter-spacing: 0.005em; }}

  .vs {{ position: absolute; top: {CIRCLE_Y + CIRCLE_D // 2 - 46}px; left: {CANVAS_W // 2 - 46}px;
         width: 92px; height: 92px; border-radius: 50%; background: #050B09;
         border: 3px solid rgba(255,255,255,0.22); color: #fff; font-weight: 700; font-size: 33px;
         display: flex; align-items: center; justify-content: center; letter-spacing: 0.04em; }}

  .kicker {{ position: absolute; top: 1338px; left: 74px; width: 932px; font-weight: 700;
             font-size: 54px; line-height: 1.18; color: #fff; }}
  .kicker span {{ color: {POP}; }}

  .cta-chip {{ position: absolute; top: 1482px; left: 74px; padding: 22px 40px; border-radius: 999px;
               background: {BRAND}; color: #fff; font-weight: 700; font-size: 36px;
               letter-spacing: 0.02em; box-shadow: 0 14px 40px rgba(4,120,87,0.45); }}

  .footer {{ position: absolute; left: 74px; bottom: 118px; width: 932px; display: flex;
             align-items: center; justify-content: space-between; }}
  .footer-site {{ font-weight: 400; font-size: 30px; color: rgba(255,255,255,0.6); }}
  .arn {{ position: absolute; left: 74px; bottom: 64px; width: 932px; font-weight: 500;
          font-size: 21px; color: rgba(255,255,255,0.5); }}

  .wordmark {{ display: inline-flex; align-items: center; }}
  .wordmark-mark {{ display: block; width: 58px; height: 58px; }}
  .wordmark-text {{ font-weight: 700; font-size: 48px; color: #fff; letter-spacing: -0.02em;
                    margin-left: 15px; }}
  .brand-img {{ display: block; width: 252px; height: auto; filter: brightness(0) invert(1); }}
</style>
</head>
<body>
<div id="stage" data-composition-id="{COMP_ID}" data-start="0" data-duration="1"
     data-fps="30" data-width="{CANVAS_W}" data-height="{CANVAS_H}">

  <div class="ghost"></div>
  <div class="ghost ghost--2"></div>

  <div class="top-mark">{brand_lockup()}</div>

  <div class="hook">{hook_html}</div>
{person("left", "anshuman.jpg", "ANSHUMAN", "PLANS FIRST", POP, LEFT_X)}
{person("right", "vedant.jpg", "VEDANT", "SPENDS FIRST", SPEND, RIGHT_X)}
  <div class="vs">VS</div>

  <div class="kicker">Which jar looks <span>like yours?</span></div>
  <div class="cta-chip">{CTA_CHIP}</div>

  <div class="footer">
    <div class="footer-site">prospur.in</div>
  </div>
  <div class="arn">{ARN_LINE}</div>
</div>
<script src="vendor/gsap.min.js"></script>
<script>
(function () {{
  // Static cover, but the runtime still expects one paused timeline
  // registered against the composition id (PLAYBOOK §9.10).
  var tl = gsap.timeline({{ paused: true }});
  tl.set('#stage', {{}}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{COMP_ID}"] = tl;
}})();
</script>
</body>
</html>
"""


def main():
    out = os.path.join(HERE, "public", "index.html")
    with open(out, "w") as f:
        f.write(HTML)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
