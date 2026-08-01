#!/usr/bin/env python3
"""
SAVER vs SPENDER — Prospur Instagram Reel.
Archetype 3 (split-screen B-roll), adapted: the source is a TOP/BOTTOM split,
not the left/right split the stock template assumes. See PLAYBOOK.md §4, §8, §9.

  top half    = Anshuman (blue shirt)  — plans first, spends less
  bottom half = Vedant   (white shirt) — spends first, plans later

Run `./build_base.sh <source.mp4>` first — it produces public/input-video.mp4
(1080x1548, reframed, half-swap corrected, audio repaired). This script builds
the overlay on top of it.

  python3 assemble.py
  npx hyperframes lint public
  npx hyperframes snapshot public --at 1.5,5,8.5,13,18,21.6,24.4
  npx hyperframes render public --skill=general-video -o output.mp4 --fps 30

LOGO
Drop the Prospur artwork at public/brand/prospur-logo.png and re-run — it is
picked up automatically. The supplied logo IS a wordmark, so no "Prospur"
text is ever set beside it. Until the file exists, a vector reconstruction
of the wordmark stands in — see brand_lockup(). Supply the light/knockout
version: no invert filter is applied, so a dark-on-white file will not read.

LAYOUT (1080x1920 canvas — Instagram Reels / 9:16)
  y    0 - 1548  video block (two halves of 774, seam at y=774)
  y 1548 - 1658  compliance strip  <- above Instagram's ~250px bottom UI band,
                                      so it survives the in-feed crop (§2)
  y 1658 - 1920  brand band — sits *under* the IG UI on purpose

All overlay chrome lives on the seam (the dead zone where two shots join) or
below the video, so nothing covers a face or a story prop — the parcels sit
bottom-left, the snacks along the desk, the SAVINGS jar bottom-right.

TRACK / Z-ORDER (data-track-index doubles as z-order in HyperFrames)
  0 video · 1-2 colour tints · 3 vignette · 4 grain · 5 cut flashes
  6 divider · 7-8 chips · 9 captions · 11-12 ring annotations
  13 hook scrim · 14 letterbox · 15 hook · 16 CTA scrim · 17 CTA
  18 compliance plate · 19 seam mark · 20 progress bar
Track 10 is left free — PLAYBOOK §9.6 reserves it for an audio element.
"""
import os

FPS = 30
CANVAS_W, CANVAS_H = 1080, 1920
VIDEO_H = 1548
SEAM_Y = 774
COMPLIANCE_TOP = 1548
BAND_TOP = 1658
DURATION = 25.2667
COMP_ID = "prospur-saver-vs-spender"

# ---- Brand tokens (PLAYBOOK.md §1) -----------------------------------------
BRAND = "#047857"     # primary green
POP = "#34D399"       # brighter mint — used over footage
SPEND = "#F59E0B"     # the spender side
SPEND_HOT = "#F87171"

COMPLIANCE_LINES = [
    "Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873",
    "Mutual funds are subject to market risks. Read all scheme-related documents carefully.",
    "For information only, not investment advice.",
]

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "public", "brand", "prospur-logo.png")

# Scene cuts detected in the source (ffmpeg scene score > 0.08)
CUTS = [6.4333, 10.50, 15.6667, 20.4333]

# ---- Copy ------------------------------------------------------------------
# No rupee figures anywhere and no named schemes: the contrast is carried by
# what is physically on screen (parcel counts, desk clutter, jar level), which
# keeps the reel clear of PLAYBOOK §2's "never invent figures" rule entirely.
# Phrasing stays non-directive — observations, not instructions.
HOOK_LINES = ["Same salary.", "Same coffee.", "Different month-end."]

# Everything overlaid on the footage clears out when the CTA takes over, so the
# closing frame is the ask and nothing else.
CTA_START = 22.80

# chip label per scene: (start, end, top_label, bottom_label)
CHIPS = [
    (3.30, 6.4333, "PLANS FIRST", "SPENDS FIRST"),
    (6.4333, 10.50, "ONE PARCEL", "PARCEL PILE"),
    # "items" not "snacks": the spender side is a protein bar, a coffee cup, a
    # bottle and an energy-bites pack — only two of the four are snacks, and a
    # caption that overstates what is on screen is not worth the extra punch.
    (10.50, 15.6667, "ONE ITEM", "FOUR ITEMS"),
    (15.6667, 20.4333, "SLEPT ON IT", "BOUGHT IT NOW"),
    (20.4333, CTA_START, "SAVES FIRST", "SAVES LAST"),
]

# right-of-seam caption per scene: (start, end, line1, line2)
CAPTIONS = [
    (3.45, 6.30, "Same coffee run.", "Only one planned for it."),
    (6.60, 10.35, "Sale week.", "Different carts."),
    (10.70, 15.50, "The small stuff", "is never the small stuff."),
    (15.85, 20.30, "One added it to cart.", "One added it to the bill."),
    # No seam caption in scene 5 — the ring annotations sit right where a
    # right-aligned caption would land, and the payoff reads better annotated
    # on the jars themselves than described next to them.
]

# Scene-5 annotations: rings drawn around the real SAVINGS jars already on
# screen — annotating the actual footage beats dropping a redundant jar SVG
# next to it. cx/cy/rx/ry are canvas pixels measured off a 21.8s frame; the
# label sits ABOVE each ring, on clean background, never over a hand or a face.
ANNOTATIONS = [
    # (start, end, cx, cy, rx, ry, colour, label, label_top)
    (20.90, CTA_START, 890, 595, 178, 172, POP, "FILLING UP", 348),
    (21.25, CTA_START, 900, 1372, 178, 166, SPEND, "STILL EMPTY", 1124),
]

CTA_LINES = ["Which jar looks", "like yours?"]
CTA_SUB = "Want to understand where yours goes?"
CTA_CHIP = "DM us  ·  Start your SIP"

CINEMA = os.environ.get("CINEMA", "1") != "0"   # debug toggle for the base layers

HOOK_END = 3.20
DIVIDER_START = 2.95


def q(t):
    """Quantize to the nearest frame."""
    return round(round(float(t) * FPS) / FPS, 3)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def words(line, cls="hw"):
    return "".join(f'<span class="{cls}">{esc(w)}</span> ' for w in line.split())


# Wordmark green — the gradient runs green into lime across the accent letter,
# matching the supplied artwork rather than the reel's own --brand/--pop pair.
MARK_G1, MARK_G2 = "#1E9E4A", "#8CC63F"


def brand_lockup(size):
    """The real artwork when it is present, otherwise a vector reconstruction
    of it: PROSPUR knocked out to white with the second letter carrying the
    green-to-lime gradient.

    Set in Inter Bold, so the letterforms approximate the real wordmark rather
    than reproduce it — this is a stand-in, not the asset. Drop the supplied
    PNG at public/brand/prospur-logo.png and it takes over automatically.

    Supply the light/knockout version: no invert filter is applied, because
    inverting would flatten the green accent letter to white along with
    everything else."""
    if os.path.exists(LOGO):
        return f'<img src="brand/prospur-logo.png" class="brand-img brand-img--{size}" alt="Prospur" />'
    gid = f"pg-{size}"
    return (
        f'<svg class="wordmark wordmark--{size}" viewBox="0 0 668 150" role="img" '
        f'aria-label="Prospur">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0.85" y2="1">'
        f'<stop offset="0" stop-color="{MARK_G1}"/><stop offset="1" stop-color="{MARK_G2}"/>'
        f'</linearGradient></defs>'
        f'<text x="4" y="116" font-family="Inter, Helvetica Neue, Arial, sans-serif" '
        f'font-weight="700" font-size="132" letter-spacing="-2" fill="#FFFFFF">'
        f'P<tspan fill="url(#{gid})">R</tspan>OSPUR</text></svg>'
    )


# ---- build ------------------------------------------------------------------

def build():
    html_parts, tl = [], []

    def clip(el_id, track, start, end, inner_cls, inner_html, extra_cls=""):
        """Emit a timed .clip element. HyperFrames owns the .clip element's own
        visibility (§9.1/§9.2) so every animation targets the inner wrapper."""
        # Quantize the endpoints FIRST, then subtract. Quantizing the duration
        # independently rounds the other way at some boundaries and pushes a
        # clip one frame past the next one's start -> overlapping_clips_same_track.
        start, end = q(start), q(end)
        html_parts.append(
            f'  <div id="{el_id}" class="clip {extra_cls}" data-track-index="{track}" '
            f'data-start="{start}" data-duration="{round(end - start, 3)}">\n'
            f'    <div class="{inner_cls}">{inner_html}</div>\n  </div>'
        )
        return start, end

    def hold(sel, at=0):
        """Pin a wrapper visible. Only for elements that some OTHER tween
        would otherwise leave mid-state — never for a static always-on
        layer, because forcing opacity:1 overrides whatever alpha its CSS
        intends (this is how the grain ended up painting at full strength
        over the footage instead of at 0.055)."""
        tl.append(f"tl.set('{sel}', {{ opacity: 1, y: 0 }}, {q(at)});")

    def exit_on(sel, end, dur=0.22):
        """Exit tween must land exactly on the hard-kill .set() — landing even a
        few ms after it trips gsap_exit_missing_hard_kill and lets the element
        flash back on seek (§6, §9.7).

        Both endpoints are quantized and the duration derived from the
        difference. Quantizing start and duration independently leaves them a
        frame out of step at some boundaries, which is exactly the failure the
        rule exists to catch."""
        end_q = q(end)
        start_q = q(end_q - dur)
        tl.append(
            f"tl.to('{sel}', {{ opacity: 0, duration: {round(end_q - start_q, 3)}, "
            f"ease: 'power2.in' }}, {start_q});"
        )
        tl.append(f"tl.set('{sel}', {{ opacity: 0, visibility: 'hidden' }}, {end_q});")

    # ---------------------------------------------------------------- video --
    html_parts.append(
        # no `muted`: the repaired room tone is the reel's audio bed
        f'  <video id="input-video" class="clip" data-track-index="0" data-start="0" '
        f'data-duration="{q(DURATION)}" data-has-audio="true" data-volume="1" '
        f'src="input-video.mp4" playsinline></video>'
    )

    # ------------------------------------------------- cinematic base layer --
    # Per-half colour grade: the saver's half runs cool green, the spender's
    # runs warm amber. Kept at soft-light and low alpha so skin still reads
    # natural — it should feel like a grade, not a filter.
    if CINEMA:
        clip("tint-top", 1, 0, DURATION, "tint-inner tint-inner--top", "")
        clip("tint-bot", 2, 0, DURATION, "tint-inner tint-inner--bot", "")

    if CINEMA:
        clip("vignette", 3, 0, DURATION, "vignette-inner", "")

    # Film grain from a pre-baked 192x192 tile (brand/noise.png), repeated.
    # Deterministic, and free to rasterize. An inline SVG feTurbulence gives a
    # nicer grain but is catastrophically slow under software rasterization —
    # it took the 25s render from ~7 minutes to over 40 with no end in sight,
    # and starved the video layer badly enough that frames composited without
    # it. Not worth it for a texture nobody consciously notices.
    if CINEMA and os.path.exists(os.path.join(HERE, "public", "brand", "noise.png")):
        clip("grain", 4, 0, DURATION, "grain-inner", "")
    
    # ------------------------------------------------------- cut flashes ----
    # A short bloom on each scene cut, plus a pulse through the divider. Sells
    # the cut as a deliberate edit rather than a jump in the source.
    for i, cut in enumerate(CUTS):
        s, e = cut - 0.02, cut + 0.26
        clip(f"flash-{i}", 5, s, e, "flash-inner", "")
        tl.append(f"tl.set('#flash-{i} .flash-inner', {{ opacity: 0 }}, {q(s)});")
        tl.append(
            f"tl.to('#flash-{i} .flash-inner', {{ opacity: 0.22, duration: 0.05, "
            f"ease: 'power2.out' }}, {q(cut)});"
        )
        peak_q, end_q = q(cut + 0.05), q(e)
        tl.append(
            f"tl.to('#flash-{i} .flash-inner', {{ opacity: 0, duration: {round(end_q - peak_q, 3)}, "
            f"ease: 'power2.in' }}, {peak_q});"
        )
        tl.append(f"tl.set('#flash-{i} .flash-inner', {{ opacity: 0, visibility: 'hidden' }}, {end_q});")

    # --------------------------------------------------------- seam divider --
    clip("divider", 6, DIVIDER_START, DURATION, "divider-inner", "")
    tl.append(
        f"tl.fromTo('.divider-inner', {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, "
        f"duration: 0.5, ease: 'power3.out' }}, {q(DIVIDER_START)});"
    )
    for cut in CUTS:
        tl.append(f"tl.to('.divider-inner', {{ scaleY: 2.8, duration: 0.09, ease: 'power2.out' }}, {q(cut)});")
        tl.append(f"tl.to('.divider-inner', {{ scaleY: 1, duration: 0.26, ease: 'power2.in' }}, {q(cut + 0.09)});")

    # --------------------------------------------------------- label chips ---
    for i, (s, e, top_label, bot_label) in enumerate(CHIPS):
        clip(
            f"chip-t-{i}", 7, s, e, "chip-inner chip-inner--top",
            f'<span class="chip-rule chip-rule--save"></span>'
            f'<span class="chip-body"><span class="chip-name">ANSHUMAN</span>'
            f'<span class="chip-label chip-label--save">{esc(top_label)}</span></span>',
        )
        clip(
            f"chip-b-{i}", 8, s, e, "chip-inner chip-inner--bot",
            f'<span class="chip-rule chip-rule--spend"></span>'
            f'<span class="chip-body"><span class="chip-name">VEDANT</span>'
            f'<span class="chip-label chip-label--spend">{esc(bot_label)}</span></span>',
        )
        for which in ("t", "b"):
            sel = f"#chip-{which}-{i} .chip-inner"
            tl.append(
                f"tl.fromTo('{sel}', {{ opacity: 0, x: -46 }}, {{ opacity: 1, x: 0, "
                f"duration: 0.42, ease: 'back.out(1.5)' }}, {q(s)});"
            )
            exit_on(sel, e)
            tl.append(
                f"tl.fromTo('#chip-{which}-{i} .chip-rule', {{ scaleY: 0 }}, {{ scaleY: 1, "
                f"duration: 0.32, ease: 'back.out(2)' }}, {q(s + 0.10)});"
            )

    # ------------------------------------------------------ scene captions ---
    for i, (s, e, l1, l2) in enumerate(CAPTIONS):
        clip(
            f"cap-{i}", 9, s, e, "cap-inner",
            f'<div class="cap-line">{words(l1, "cw")}</div>'
            f'<div class="cap-line cap-line--2">{words(l2, "cw")}</div>',
        )
        tl.append(
            f"tl.fromTo('#cap-{i} .cap-inner', {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, "
            f"duration: 0.26, ease: 'power2.out' }}, {q(s)});"
        )
        tl.append(
            f"tl.fromTo('#cap-{i} .cw', {{ opacity: 0, y: 18, scale: 0.94 }}, {{ opacity: 1, y: 0, "
            f"scale: 1, duration: 0.3, ease: 'back.out(1.7)', stagger: 0.05 }}, {q(s + 0.06)});"
        )
        exit_on(f"#cap-{i} .cap-inner", e)

    # ---------------------------------------------------- scene-5 ring SVG ---
    for i, (s, e, cx, cy, rx, ry, colour, label, label_top) in enumerate(ANNOTATIONS):
        svg = (
            f'<svg class="ring-svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" aria-hidden="true">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{colour}" '
            f'stroke-width="7" stroke-linecap="round" transform="rotate(-9 {cx} {cy})"/>'
            f'<path d="M{cx + 30} {cy - ry - 8} L{cx + 8} {label_top + 74}" stroke="{colour}" '
            f'stroke-width="5" stroke-linecap="round" fill="none"/></svg>'
            f'<span class="ring-label" style="top:{label_top}px; color:{colour};">{esc(label)}</span>'
        )
        clip(f"ring-{i}", 11 + i, s, e, "ring-inner", svg)
        tl.append(
            f"tl.fromTo('#ring-{i} .ring-inner', {{ opacity: 0, scale: 1.24, rotation: -3 }}, "
            f"{{ opacity: 1, scale: 1, rotation: 0, duration: 0.46, ease: 'back.out(1.6)' }}, {q(s)});"
        )
        exit_on(f"#ring-{i} .ring-inner", e)

    # ------------------------------------------------------------ the hook --
    clip("hook-scrim", 13, 0, HOOK_END, "hook-scrim-inner", "")
    hold(".hook-scrim-inner")
    exit_on(".hook-scrim-inner", HOOK_END, 0.32)

    # cinematic letterbox that rides in with the hook and pulls away with it
    clip("letterbox", 14, 0, HOOK_END, "lb-inner", '<div class="lb lb--t"></div><div class="lb lb--b"></div>')
    tl.append("tl.set('.lb-inner', { opacity: 1, y: 0 }, 0);")
    tl.append("tl.fromTo('.lb--t', { y: -128 }, { y: 0, duration: 0.5, ease: 'power3.out' }, 0);")
    tl.append("tl.fromTo('.lb--b', { y: 128 }, { y: 0, duration: 0.5, ease: 'power3.out' }, 0);")
    tl.append(f"tl.to('.lb--t', {{ y: -128, duration: 0.34, ease: 'power2.in' }}, {q(HOOK_END - 0.34)});")
    tl.append(f"tl.to('.lb--b', {{ y: 128, duration: 0.34, ease: 'power2.in' }}, {q(HOOK_END - 0.34)});")
    tl.append(f"tl.set('.lb-inner', {{ opacity: 0, visibility: 'hidden' }}, {q(HOOK_END)});")

    hook_html = "".join(
        f'<div class="hook-line hook-line--{i}">{words(l)}</div>' for i, l in enumerate(HOOK_LINES)
    )
    clip("hook", 15, 0, HOOK_END, "hook-inner", hook_html)
    hold(".hook-inner")
    for i in range(len(HOOK_LINES)):
        # First word is up by frame 3 — a quarter-second of empty scrim at the
        # top of a Reel is a quarter-second of people scrolling past it.
        at = q(0.10 + 0.62 * i)
        tl.append(
            f"tl.fromTo('.hook-line--{i} .hw', {{ opacity: 0, y: 30, scale: 0.88 }}, "
            f"{{ opacity: 1, y: 0, scale: 1, duration: 0.38, ease: 'back.out(2)', stagger: 0.065 }}, {at});"
        )
    exit_on(".hook-inner", HOOK_END, 0.28)

    # ------------------------------------------------------------- the CTA ---
    clip("cta-scrim", 16, CTA_START, DURATION, "cta-scrim-inner", "")
    tl.append(
        f"tl.fromTo('.cta-scrim-inner', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.34, "
        f"ease: 'power2.out' }}, {q(CTA_START)});"
    )
    cta_html = (
        "".join(f'<div class="cta-line">{words(l, "kw")}</div>' for l in CTA_LINES)
        + f'<div class="cta-sub">{esc(CTA_SUB)}</div>'
        + f'<div class="cta-chip">{esc(CTA_CHIP)}</div>'
    )
    clip("cta", 17, CTA_START, DURATION, "cta-inner", cta_html)
    hold(".cta-inner", CTA_START)
    tl.append(
        f"tl.fromTo('.cta-line .kw', {{ opacity: 0, y: 28, scale: 0.9 }}, {{ opacity: 1, y: 0, "
        f"scale: 1, duration: 0.36, ease: 'back.out(1.9)', stagger: 0.055 }}, {q(CTA_START + 0.12)});"
    )
    tl.append(
        f"tl.fromTo('.cta-sub', {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, "
        f"ease: 'power2.out' }}, {q(CTA_START + 0.62)});"
    )
    tl.append(
        f"tl.fromTo('.cta-chip', {{ opacity: 0, y: 18, scale: 0.9 }}, {{ opacity: 1, y: 0, "
        f"scale: 1, duration: 0.4, ease: 'back.out(2.2)' }}, {q(CTA_START + 0.84)});"
    )
    # one slow breath on the chip so the last second is not a frozen frame
    tl.append(f"tl.to('.cta-chip', {{ scale: 1.05, duration: 0.55, ease: 'sine.inOut' }}, {q(CTA_START + 1.36)});")
    tl.append(f"tl.to('.cta-chip', {{ scale: 1.0, duration: 0.55, ease: 'sine.inOut' }}, {q(CTA_START + 1.91)});")

    # ------------------------------------------- compliance + brand plate ----
    compliance_html = (
        '<div class="plate-rule"></div>'
        + '<div class="compliance">'
        + "".join(f'<div class="compliance-line">{esc(t)}</div>' for t in COMPLIANCE_LINES)
        + "</div>"
        + '<div class="band">'
        + f'<div class="band-left">{brand_lockup("band")}</div>'
        + '<div class="band-right"><span class="band-dot"></span>prospur.in</div>'
        + "</div>"
    )
    clip("plate", 18, 0, DURATION, "plate-inner", compliance_html)

    # ------------------------------------------------- seam brand watermark --
    # In-feed, Instagram's UI covers the brand band at the bottom, so a small
    # mark also rides the seam — the one strip of frame that is never a face.
    clip("seam-mark", 19, DIVIDER_START, DURATION, "seam-mark-inner", brand_lockup("seam"))
    tl.append(
        f"tl.fromTo('.seam-mark-inner', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, "
        f"ease: 'power2.out' }}, {q(DIVIDER_START + 0.2)});"
    )

    # ------------------------------------------------------- retention bar --
    clip("progress", 20, 0, DURATION, "progress-inner", '<div class="progress-fill"></div>')
    tl.append(
        f"tl.fromTo('.progress-fill', {{ scaleX: 0 }}, {{ scaleX: 1, duration: {q(DURATION)}, "
        f"ease: 'none' }}, 0);"
    )

    return "\n".join(html_parts), "\n  ".join(tl)


BODY, TIMELINE = build()

CSS = f"""
  @font-face {{ font-family: 'Inter'; src: url('fonts/Inter-Regular.woff2') format('woff2');
               font-weight: 400; font-style: normal; font-display: block; }}
  @font-face {{ font-family: 'Inter'; src: url('fonts/Inter-Bold.woff2') format('woff2');
               font-weight: 700; font-style: normal; font-display: block; }}

  html, body {{ margin: 0; padding: 0; background: #050B09; }}
  /* concrete family names, never a CSS var — the font analyzer cannot expand
     vars and would flag font_family_without_font_face (§9.3) */
  #stage {{ position: relative; width: {CANVAS_W}px; height: {CANVAS_H}px; overflow: hidden;
            background: #050B09; font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; }}

  video#input-video {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px;
                       height: {VIDEO_H}px; object-fit: cover; }}

  /* ---- cinematic base layer ---- */
  /* NO mix-blend-mode anywhere over the video. Chromium promotes <video> to
     its own compositing layer, and a blended element above it composites
     WITHOUT that layer in its backdrop — the whole video block renders as a
     flat white plate. Cost us a render to find. Plain alpha only. */
  .tint-inner {{ position: absolute; left: 0; width: {CANVAS_W}px; height: {SEAM_Y}px;
                 pointer-events: none; }}
  .tint-inner--top {{ top: 0;
      background: linear-gradient(180deg, rgba(16,185,129,0.20) 0%, rgba(6,78,59,0.07) 100%); }}
  .tint-inner--bot {{ top: {SEAM_Y}px;
      background: linear-gradient(0deg, rgba(245,158,11,0.20) 0%, rgba(120,53,15,0.07) 100%); }}

  .vignette-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {VIDEO_H}px;
      background: radial-gradient(ellipse 76% 56% at 50% 50%,
                  rgba(0,0,0,0) 40%, rgba(0,0,0,0.20) 74%, rgba(0,0,0,0.52) 100%); }}

  .grain-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {VIDEO_H}px;
                  opacity: 0.055; background-image: url('brand/noise.png');
                  background-repeat: repeat; background-size: 192px 192px; }}

  .flash-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {VIDEO_H}px;
                  background: linear-gradient(180deg, rgba(255,255,255,0.96) 0%,
                              rgba(214,255,238,0.9) 50%, rgba(255,255,255,0.96) 100%); }}

  /* ---- hook ---- */
  /* Light enough that the café still reads through — the first three seconds
     decide whether the reel gets watched, and a near-black opening frame
     looks like a loading screen in-feed. Legibility comes back via the text
     shadow on .hook-line rather than more scrim. */
  .hook-scrim-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {VIDEO_H}px;
                       background: linear-gradient(180deg, rgba(4,10,8,0.78) 0%, rgba(4,10,8,0.52) 50%,
                                                   rgba(4,10,8,0.78) 100%); }}
  .lb-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {VIDEO_H}px; }}
  .lb {{ position: absolute; left: 0; width: {CANVAS_W}px; height: 128px; background: #04100C; }}
  .lb--t {{ top: 0; }}
  .lb--b {{ bottom: 0; }}

  .hook-inner {{ position: absolute; top: 430px; left: 72px; width: 936px; text-align: left; }}
  .hook-line {{ font-weight: 700; font-size: 92px; line-height: 1.12; color: #fff; letter-spacing: -0.015em;
                text-shadow: 0 3px 18px rgba(0,0,0,0.9), 0 0 46px rgba(0,0,0,0.7); }}
  .hook-line--2 {{ color: {POP}; }}
  .hook-line .hw {{ display: inline-block; margin: 0 0.19em 0 0; }}

  /* ---- seam ---- */
  .divider-inner {{ position: absolute; top: {SEAM_Y - 3}px; left: 0; width: {CANVAS_W}px; height: 6px;
                    background: #fff; box-shadow: 0 0 22px 3px rgba(52,211,153,0.85); }}

  .chip-inner {{ position: absolute; left: 32px; width: 400px; height: 96px; display: flex;
                 align-items: center; gap: 16px; padding: 0 20px 0 0;
                 background: rgba(6,14,11,0.74); border-radius: 14px;
                 backdrop-filter: blur(2px); box-sizing: border-box; }}
  .chip-inner--top {{ top: {SEAM_Y - 108}px; }}
  .chip-inner--bot {{ top: {SEAM_Y + 14}px; }}
  .chip-rule {{ width: 7px; height: 60px; border-radius: 4px; flex: 0 0 auto; margin-left: 16px;
                transform-origin: center center; }}
  .chip-rule--save {{ background: {POP}; box-shadow: 0 0 14px rgba(52,211,153,0.7); }}
  .chip-rule--spend {{ background: {SPEND}; box-shadow: 0 0 14px rgba(245,158,11,0.7); }}
  .chip-body {{ display: flex; flex-direction: column; justify-content: center; }}
  .chip-name {{ font-weight: 400; font-size: 17px; letter-spacing: 0.16em;
                color: rgba(255,255,255,0.62); margin-bottom: 3px; }}
  .chip-label {{ font-weight: 700; font-size: 31px; letter-spacing: 0.005em; line-height: 1.05; }}
  .chip-label--save {{ color: {POP}; }}
  .chip-label--spend {{ color: {SPEND}; }}

  .cap-inner {{ position: absolute; left: 452px; top: {SEAM_Y - 116}px; width: 596px;
                text-align: right; }}
  .cap-line {{ font-weight: 700; font-size: 40px; line-height: 1.2; color: #fff;
               text-shadow: 0 2px 14px rgba(0,0,0,0.85), 0 0 34px rgba(0,0,0,0.6); }}
  .cap-line--2 {{ color: rgba(255,255,255,0.82); }}
  .cap-line .cw {{ display: inline-block; margin: 0 0 0 0.2em; }}

  .seam-mark-inner {{ position: absolute; right: 32px; top: {SEAM_Y + 26}px; }}

  /* ---- scene-5 ring annotations ---- */
  .ring-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {CANVAS_H}px;
                 transform-origin: center center; }}
  .ring-svg {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {CANVAS_H}px;
               filter: drop-shadow(0 2px 10px rgba(0,0,0,0.55)); }}
  /* label rides above its ring on a dark plate — amber on a white shirt has
     nowhere near enough contrast on its own */
  .ring-label {{ position: absolute; right: 32px; padding: 12px 22px; border-radius: 12px;
                 background: rgba(6,14,11,0.78); font-weight: 700; font-size: 36px;
                 letter-spacing: 0.05em; text-shadow: 0 2px 12px rgba(0,0,0,0.85); }}

  /* ---- CTA ---- */
  .cta-scrim-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: {VIDEO_H}px;
                      background: linear-gradient(180deg, rgba(4,10,8,0.86) 0%, rgba(4,10,8,0.78) 100%); }}
  .cta-inner {{ position: absolute; top: 470px; left: 72px; width: 936px; }}
  .cta-line {{ font-weight: 700; font-size: 88px; line-height: 1.1; color: #fff; letter-spacing: -0.015em;
               text-shadow: 0 3px 18px rgba(0,0,0,0.85); }}
  .cta-line .kw {{ display: inline-block; margin: 0 0.19em 0 0; }}
  .cta-sub {{ margin-top: 26px; font-weight: 400; font-size: 36px; line-height: 1.35;
              color: rgba(255,255,255,0.86); }}
  .cta-chip {{ display: inline-block; margin-top: 34px; padding: 20px 34px; border-radius: 999px;
               background: {BRAND}; color: #fff; font-weight: 700; font-size: 34px;
               letter-spacing: 0.02em; box-shadow: 0 10px 34px rgba(4,120,87,0.55);
               transform-origin: left center; }}

  /* ---- compliance + brand plate ---- */
  .plate-inner {{ position: absolute; top: {COMPLIANCE_TOP}px; left: 0; width: {CANVAS_W}px;
                  height: {CANVAS_H - COMPLIANCE_TOP}px; background: #06100D; }}
  .plate-rule {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: 4px;
                 background: linear-gradient(90deg, {BRAND} 0%, {POP} 55%, {BRAND} 100%); }}
  .compliance {{ position: absolute; top: 18px; left: 44px; width: {CANVAS_W - 88}px; }}
  .compliance-line {{ font-weight: 500; font-size: 20px; line-height: 1.42;
                      color: rgba(255,255,255,0.86); text-shadow: 0 1px 4px rgba(0,0,0,0.7); }}
  .band {{ position: absolute; top: {BAND_TOP - COMPLIANCE_TOP + 26}px; left: 44px;
           width: {CANVAS_W - 88}px; display: flex; align-items: center;
           justify-content: space-between; }}
  .band-right {{ display: flex; align-items: center; gap: 12px; font-weight: 400; font-size: 30px;
                 color: rgba(255,255,255,0.62); }}
  .band-dot {{ width: 12px; height: 12px; border-radius: 50%; background: {POP}; display: inline-block; }}

  /* ---- retention progress bar ---- */
  .progress-inner {{ position: absolute; top: 0; left: 0; width: {CANVAS_W}px; height: 6px;
                     background: rgba(255,255,255,0.16); }}
  .progress-fill {{ width: 100%; height: 100%; background: {POP};
                    transform-origin: left center; box-shadow: 0 0 14px {POP}; }}

  /* ---- brand mark (real artwork drops in at public/brand/prospur-logo.png) ----
     No invert filter: supply the light/knockout version. Inverting a
     dark-on-white logo would flatten the green accent letter to white too. */
  .brand-img, .wordmark {{ display: block; height: auto; }}
  .brand-img--band, .wordmark--band {{ width: 300px; }}
  .brand-img--seam, .wordmark--seam {{ width: 178px; opacity: 0.94;
                      filter: drop-shadow(0 2px 9px rgba(0,0,0,0.95)); }}
"""

HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Prospur — Saver vs Spender</title>
<style>{CSS}</style>
</head>
<body>
<div id="stage" data-composition-id="{COMP_ID}" data-start="0" data-duration="{q(DURATION)}"
     data-fps="{FPS}" data-width="{CANVAS_W}" data-height="{CANVAS_H}">
{BODY}
</div>
<script src="vendor/gsap.min.js"></script>
<script>
(function () {{
  var tl = gsap.timeline({{ paused: true }});
  {TIMELINE}
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
    print(f"  {q(DURATION)}s @ {FPS}fps · {CANVAS_W}x{CANVAS_H} (Instagram Reels 9:16)")
    print(f"  {len(CHIPS)} chip pairs · {len(CAPTIONS)} captions · {len(ANNOTATIONS)} rings · {len(CUTS)} cut flashes")
    print(f"  logo: {'brand/prospur-logo.png' if os.path.exists(LOGO) else 'MISSING — using the vector wordmark reconstruction'}")


if __name__ == "__main__":
    main()
