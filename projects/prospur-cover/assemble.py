#!/usr/bin/env python3
"""
Reels cover for the SAVER vs SPENDER reel — Archetype 4 (PLAYBOOK.md §4).
Renders to a single 1080x1920 PNG, not an MP4.

  python3 assemble.py
  npx hyperframes lint public
  npx hyperframes snapshot public --at 0

LOGO
Drop the Prospur artwork at public/img/prospur-logo.png and re-run — it is
picked up automatically. The wordmark IS the logo, so no "Prospur" text is
ever set beside it. Until the file exists a plain green mark stands in.

CROP SAFETY
Instagram crops a cover three ways: the Reels player shows the full
1080x1920, the feed takes a centred 4:5 slice (~y285-1635), and the profile
grid takes a centred 1:1 slice (~y420-1500). Both figures and both labels
sit inside the 1:1 band, so the comparison survives every crop; the hook
clears the 4:5 top edge.
"""
import os

CANVAS_W, CANVAS_H = 1080, 1920
COMP_ID = "prospur-cover"

BRAND = "#047857"
POP = "#34D399"
SPEND = "#F59E0B"

HOOK_LINES = [
    ("Same salary.", "hook-line--white"),
    ("Different", "hook-line--pop"),
    ("month-end.", "hook-line--pop"),
]
ARN_LINE = "Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873"
CTA_CHIP = "DM us  ·  Start your SIP"

# full-body panels, both inside the ~y420-1500 profile-grid band
PANEL_W, PANEL_H = 452, 856
PANEL_Y = 600
LEFT_X, RIGHT_X = 74, 554

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "public", "img", "prospur-logo.png")


def brand_lockup():
    """The real artwork when it is present. No 'Prospur' text is set next to
    it — the supplied logo is itself a wordmark, so typing the name again
    would double it up."""
    if os.path.exists(LOGO):
        return '<img src="img/prospur-logo.png" class="brand-img" alt="Prospur" />'
    return (
        f'<svg class="brand-fallback" viewBox="0 0 40 40" aria-hidden="true">'
        f'<rect x="1.5" y="1.5" width="37" height="37" rx="11" fill="{BRAND}"/>'
        f'<path d="M11 26.5 L18 19 L23 24 L30.5 14.5" fill="none" stroke="#fff" '
        f'stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="30.5" cy="14.5" r="2.9" fill="{POP}"/></svg>'
    )


def panel(side, img, name, label, colour, x):
    return f"""
    <div class="panel panel--{side}" style="left:{x}px; border-color:{colour};">
      <img src="img/{img}" class="panel-img" alt="{name}" />
      <div class="panel-scrim"></div>
      <div class="panel-caption">
        <div class="panel-name">{name}</div>
        <div class="panel-label" style="color:{colour};">{label}</div>
      </div>
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
              radial-gradient(1150px 800px at 16% 4%, rgba(4,120,87,0.46) 0%, rgba(5,11,9,0) 62%),
              radial-gradient(950px 720px at 94% 92%, rgba(245,158,11,0.22) 0%, rgba(5,11,9,0) 60%),
              linear-gradient(168deg, #08150F 0%, #050B09 55%, #04100C 100%); }}

  /* decorative texture only, never load-bearing */
  .ghost {{ position: absolute; top: -240px; right: -290px; width: 920px; height: 920px;
            border-radius: 50%; border: 76px solid {POP}; opacity: 0.075; }}
  .ghost--2 {{ top: auto; bottom: -320px; left: -310px; right: auto; width: 780px; height: 780px;
               border: 64px solid {SPEND}; opacity: 0.06; }}

  .top-mark {{ position: absolute; top: 78px; left: 74px; }}
  .brand-img {{ display: block; width: 300px; height: auto; filter: brightness(0) invert(1); }}
  .brand-fallback {{ display: block; width: 62px; height: 62px; }}

  /* hook sits high so it clears the 4:5 feed crop (~y285) */
  .hook {{ position: absolute; top: 246px; left: 74px; width: 932px; }}
  .hook-line {{ font-weight: 700; font-size: 94px; line-height: 1.08; letter-spacing: -0.022em; }}
  .hook-line--white {{ color: #fff; }}
  .hook-line--pop {{ color: {POP}; }}

  .panel {{ position: absolute; top: {PANEL_Y}px; width: {PANEL_W}px; height: {PANEL_H}px;
            border-radius: 30px; border: 6px solid; overflow: hidden;
            box-shadow: 0 26px 70px rgba(0,0,0,0.6); }}
  .panel-img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .panel-scrim {{ position: absolute; left: 0; right: 0; bottom: 0; height: 300px;
                  background: linear-gradient(0deg, rgba(4,10,8,0.94) 0%, rgba(4,10,8,0.55) 46%,
                                              rgba(4,10,8,0) 100%); }}
  .panel-caption {{ position: absolute; left: 26px; right: 20px; bottom: 26px; }}
  .panel-name {{ font-weight: 400; font-size: 23px; letter-spacing: 0.17em;
                 color: rgba(255,255,255,0.66); }}
  .panel-label {{ margin-top: 6px; font-weight: 700; font-size: 40px; line-height: 1.06;
                  letter-spacing: 0.005em; }}

  .vs {{ position: absolute; top: {PANEL_Y + PANEL_H // 2 - 42}px; left: {CANVAS_W // 2 - 42}px;
         width: 84px; height: 84px; border-radius: 50%; background: #050B09;
         border: 3px solid rgba(255,255,255,0.24); color: #fff; font-weight: 700; font-size: 30px;
         display: flex; align-items: center; justify-content: center; letter-spacing: 0.04em;
         box-shadow: 0 8px 26px rgba(0,0,0,0.6); }}

  .kicker {{ position: absolute; top: 1512px; left: 74px; width: 932px; font-weight: 700;
             font-size: 52px; line-height: 1.16; color: #fff; }}
  .kicker span {{ color: {POP}; }}

  .cta-chip {{ position: absolute; top: 1626px; left: 74px; padding: 20px 38px; border-radius: 999px;
               background: {BRAND}; color: #fff; font-weight: 700; font-size: 34px;
               letter-spacing: 0.02em; box-shadow: 0 14px 40px rgba(4,120,87,0.45); }}

  .footer-site {{ position: absolute; left: 74px; bottom: 108px; font-weight: 400; font-size: 28px;
                  color: rgba(255,255,255,0.58); }}
  .arn {{ position: absolute; left: 74px; bottom: 58px; width: 932px; font-weight: 500;
          font-size: 20px; color: rgba(255,255,255,0.48); }}
</style>
</head>
<body>
<div id="stage" data-composition-id="{COMP_ID}" data-start="0" data-duration="1"
     data-fps="30" data-width="{CANVAS_W}" data-height="{CANVAS_H}">

  <div class="ghost"></div>
  <div class="ghost ghost--2"></div>

  <div class="top-mark">{brand_lockup()}</div>
  <div class="hook">{hook_html}</div>
{panel("left", "anshuman.jpg", "ANSHUMAN", "PLANS FIRST", POP, LEFT_X)}
{panel("right", "vedant.jpg", "VEDANT", "SPENDS FIRST", SPEND, RIGHT_X)}
  <div class="vs">VS</div>

  <div class="kicker">Which jar looks <span>like yours?</span></div>
  <div class="cta-chip">{CTA_CHIP}</div>

  <div class="footer-site">prospur.in</div>
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
    print(f"  logo: {'img/prospur-logo.png' if os.path.exists(LOGO) else 'MISSING — using mark-only fallback'}")


if __name__ == "__main__":
    main()
