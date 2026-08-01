# Prospur Reel System — Playbook

This is the full playbook. Read it before writing or editing any composition.
Every non-obvious rule below was learned from a real failure — do not skip them.

---

## 1 · Brand identity (locked)

| Token | Value | Where it's used |
|---|---|---|
| `--brand` | `#047857` | Primary green — chips, rules, CTAs, wordmark accents |
| `--pop` | `#34D399` | Brighter mint — used **over footage** (`#047857` is too dark to read on video) |
| `--spend` (amber) | `#F59E0B` | The "spender" side in comparison reels |
| `--spend-hot` (red) | `#F87171` | Bad-outcome accents, "REALITY CHECK" chips |
| `--text` (dark) | `#16211C` | Dark backgrounds (editorial) |
| `--paper` | `#F3EDE1` | Off-white ground for editorial reels |
| **Body font** | Inter 400/700 | Everything on-footage |
| **Editorial font** | Source Serif 4 500/600 | Faceless-explainer reels |

Both fonts are bundled in `assets/fonts/`. Never fetch fonts from the network — HyperFrames' lint blocks external `src=` URLs, and Google Fonts CDN is unreliable in the headless render.

**Prospur wordmark**: `assets/prospur-logo.png` (880×168 PNG with alpha). White-on-dark treatment uses `filter: brightness(0) invert(1)`.

**AMFI registration number**: `ARN-348873`. Prospur is a **Mutual Fund Distributor**, not an advisor.

---

## 2 · Compliance (non-negotiable)

**The compliance strip must appear on every reel for its full duration.** Verbatim:

```
Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873
Mutual funds are subject to market risks. Read all scheme-related documents carefully.
For information only, not investment advice.
```

Placed bottom-of-frame with a dark gradient scrim behind it. Small Inter 500, ~19–21px on the 1920-tall canvas, `color: rgba(255,255,255,0.86)` with text-shadow.

### Content rules

- **Never invent return figures** or fund performance. If the speaker cites a number, keep their exact wording. If you need illustrative amounts in graphics, either mask them (`₹•••`) or clearly label the whole panel `ILLUSTRATIVE ONLY`.
- **No named schemes / AMCs** on-screen unless the speaker names them.
- **Use non-directive phrasing** on cards: *"may suit"*, *"want to understand"*, *"here's what to check"*. Never *"you should"*, *"buy this"*, *"guaranteed"*.
- **Bad advice from third parties** (family, friends, "finance bros") is fine to depict as long as it's clearly attributed to them, not to Prospur.

**"Start your SIP"** is acceptable as a CTA because SIP is a generic category, not a scheme.

### Instagram caveat

The compliance strip sits at the very bottom. Instagram's in-feed UI (caption, username, buttons) overlays the bottom ~250px. For guaranteed in-feed visibility, lift the strip to `bottom: y=1500` (still bottom of composition, clear of the UI overlay). Current default keeps it at `bottom: 44px` — the full frame will always show it, but in-feed will crop the bottom line.

---

## 3 · Audio spec

- **Target loudness**: −14 LUFS integrated, true-peak −1.5 dBTP (Instagram's target).
- **Common source problems** (all seen in the Prospur clips):
  - **Too quiet** (−25 to −33 LUFS) — mic held loosely, ambient room. Fix chain in §7.
  - **Clipping** (peak > −1 dBFS) — mic gain too high. Use `adeclip` before the rest of the chain.
  - **Both** — some clips are quiet AND have loud sibilants. Chain in §7 handles this.
- **Never trust Whisper's transcript from an unrepaired quiet clip** — it hallucinates. Always repair first, transcribe second.
- **"Fix voice" from HyperFrames?** — No. HyperFrames has `tts` and `transcribe`, no denoise/enhance. Repair is done in ffmpeg by hand (recipe below) or in Adobe Express (if signed in via MCP).

---

## 4 · The four archetypes (which template to use)

**Match the source to an archetype, clone that template, then adapt.**

### Archetype 1: talking-head (single-person spoken reel)
- **Input**: MP4 with one person speaking to camera.
- **Template**: `templates/01-talking-head/`
- **Skill**: `/talking-head-recut`
- **Uses**: karaoke word-pop captions, kicker chips, kinetic titles, lower-third name card, sticky brand mark, compliance strip.
- **Examples in `reference-renders/`**: `prospur-founder-recut.mp4`, `prospur-tp-recut.mp4`, `prospur-diversification.mp4`, `prospur-vedant-2.mp4`, `prospur-anshuman-2.mp4`.

### Archetype 2: faceless explainer (no footage — pure text/motion)
- **Input**: A topic or brief; no video.
- **Template**: `templates/02-faceless-explainer/`
- **Skill**: `/faceless-explainer`
- **Uses**: Editorial serif type, kinetic bars/charts/circles, hand-drawn SVG diagrams, cross-dissolve transitions, warm-paper background.
- **Example in `reference-renders/`**: (none rendered in the kit — see `flexi-cap-explained` in the original workspace for a reference build).

### Archetype 3: split-screen B-roll (silent footage with kinetic text)
- **Input**: Silent B-roll (usually a spender-vs-saver, before-vs-after, etc.).
- **Template**: `templates/03-split-broll/`
- **Skill**: `/general-video`
- **Uses**: Vertical split with a divider slide-in, paired label chips, running counters, jar-fill SVG, kinetic word-pop hook, music bed.
- **Examples**: `prospur-savings-broll.mp4` (SAVER│SPENDER), `prospur-savings-broll-2.mp4` (HABIT│TOMORROW).

### Archetype 4: still Reels cover (thumbnail)
- **Input**: A clean frame of the presenter + a hook headline.
- **Template**: `templates/04-cover/`
- **Skill**: `/motion-graphics` (rendered as a single-frame snapshot, not an MP4)
- **Uses**: Photo + top hook + ghost background element + name tag + Prospur wordmark.
- **Reminder**: Instagram crops covers three ways — Reels player (full 1080×1920), feed (4:5 slice), profile grid (1:1 centre). Keep the title in the **upper band** so it survives the 4:5 crop; the grid square only shows the centre third.

---

## 5 · Layout, safe-zones, legibility

**Canvas**: 1080×1920 (Reels) unless the archetype says otherwise. Covers are also 1080×1920. Cover-for-profile-grid crops are handled at post-time.

**Safe-zones for talking-head clips** — where you place graphics depends on where the person's head is:
- **Head starts around y=470–700** (standing, chest-up): cards live in the top 640px, captions in a low band at y=1380, compliance at y=1770.
- **Head starts around y=900** (seated, wide framing): cards live in the top 1020px, captions at y=1380, compliance at y=1770.

**Legibility scrim**: bright windows / outdoor light behind speakers wreck white text. Always overlay a top-down gradient scrim tuned to the person's head position (see `templates/01-talking-head/public/cards/card-scrim.html` — the `height:` value equals how far down you can grade).

**Never place a card over the mouth or eyes.** Never place a compliance strip over the mouth.

---

## 6 · Captions (the Whisper offset)

Whisper's word-start timestamps are consistently **~0.3 seconds early**. If you build karaoke captions straight from `transcript.json`, every line will hit before the person actually says the word.

**Fix — apply a global offset in the assembler:**

```python
CAP_OFFSET = 0.34   # tune 0.28–0.36 per clip; 0.34 is a good default
```

Karaoke word-highlight loop (Inter 700, 56–58px, low-band, per-word span):

```python
# each word turns brand green as it's spoken, then returns
for wi in range(n_words):
    t = q(s + 0.04 + span * wi / n_words)
    stmts.append(f"tl.to('#{cid}-w{wi}', {{ color: '#34D399', scale: 1.12, duration: 0.10, ease: 'power2.out', overwrite: 'auto' }}, {t});")
    stmts.append(f"tl.to('#{cid}-w{wi}', {{ scale: 1.0, duration: 0.13, ease: 'power2.in', overwrite: 'auto' }}, {q(t + 0.11)});")
```

**Word spacing**: use `margin: 0 0.19em` on each `.w` span. Anything tighter and words like "the uncle" render as "theuncle".

**Fade out must land on the hard-kill:**

```python
tl.to('#cap-X', { opacity: 0, duration: 0.12, ease: 'power2.in' }, q(end - 0.12))
tl.set('#cap-X', { opacity: 0, visibility: 'hidden' }, end)
```

If the fade tween ends *after* the hard-kill, HyperFrames lint throws `gsap_exit_missing_hard_kill` and the caption can flash back on seek.

---

## 7 · Audio repair (ffmpeg chain)

### Standard chain (works for most quiet-but-clean sources)

```bash
ffmpeg -y -i in.mp4 -map 0:a:0 \
  -af "highpass=f=85,afftdn=nr=12:nf=-30,deesser=i=0.3,acompressor=threshold=-18dB:ratio=3:attack=8:release=180:makeup=1.5,loudnorm=I=-14:TP=-1.5:LRA=11" \
  -ar 48000 -ac 2 fixed.wav
```

### Clipping source (peaks near 0 dBFS)
Prepend `adeclip`:

```bash
-af "adeclip,highpass=f=85,afftdn=nr=12:nf=-30,..."
```

### Two-pass loudness lock (belt-and-braces)

```bash
ffmpeg -y -i fixed.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" final.wav
```

### Verify

```bash
ffmpeg -nostats -i final.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "^ +(I|Peak):"
# Want: I ≈ -14, Peak ≤ -1.5
```

### Base clip build (audio + video with brightness lift + seek-safe keyframes)

```bash
ffmpeg -y -i in.mp4 -i final.wav -map 0:v:0 -map 1:a:0 \
  -vf "scale=1080:1920:flags=lanczos,eq=brightness=0.045:contrast=1.045:saturation=1.06:gamma=1.05" \
  -c:v libx264 -preset slow -crf 19 -g 30 -keyint_min 30 -pix_fmt yuv420p \
  -movflags +faststart -c:a aac -b:a 192k public/input-video.mp4
```

`-g 30 -keyint_min 30` = a keyframe every second at 30fps. Sparse GOPs freeze mid-scene when HyperFrames seeks; dense GOPs don't.

The brightness recipe `eq=brightness=0.045:contrast=1.045:saturation=1.06:gamma=1.05` is the "slight lift" every clip in this system uses. Don't push higher — it starts to look processed.

---

## 8 · Split-screen recipe (Archetype 3)

Two source clips → 540×1920 halves → hstack → mux music.

```bash
# LEFT (SAVER / positive side) — slow-loop one clean segment so the character stays consistent
ffmpeg -y -ss 20.7 -to 22.5 -i in.mp4 -an \
  -vf "eq=brightness=0.05:contrast=1.05:saturation=1.08:gamma=1.06,setpts=5.5*PTS" -r 30 saver.mp4
ffmpeg -y -stream_loop -1 -i saver.mp4 -t 25.5 saver_loop.mp4

# RIGHT (SPENDER / negative side) — the montage part of the source
ffmpeg -y -ss 0 -to 19 -i in.mp4 -an \
  -vf "eq=brightness=0.05:contrast=1.05:saturation=1.08:gamma=1.06,setpts=1.34*PTS,trim=duration=25.5" -r 30 spender.mp4

# Stitch + mux music bed
ffmpeg -y -i saver_loop.mp4 -i spender.mp4 -i music_bed.m4a \
  -filter_complex "[0:v]crop=iw*0.55:ih:iw*0.22:0,scale=540:1920[l]; \
                   [1:v]crop=iw*0.55:ih:iw*0.28:0,scale=540:1920[r]; \
                   [l][r]hstack=inputs=2,format=yuv420p[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 19 -g 30 -keyint_min 30 \
  -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k -shortest -t 25.25 public/input-video.mp4
```

Tune the `crop iw*0.22 / iw*0.28` offsets so each half is centered on the subject, not the background. The divider glow between them is a 6px white bar with a green box-shadow — see `templates/03-split-broll/public/index.html`.

### Character consistency

If the source has multiple people, **isolate one person on each half**. Otherwise the "one person's journey" reading breaks. Slow-loop a short clean segment of that person's shot; don't try to cover 25s of one side from 25s of source.

---

## 9 · HyperFrames rules (from lint, learned the hard way)

1. **Every timed element needs `class="clip"`** alongside its own classes. Without it, the element is visible for the whole comp. Lint: `timed_element_missing_clip_class`.
2. **Never animate `visibility` or `opacity` on a `.clip` element.** HyperFrames manages that. Animate an *inner* wrapper instead. Lint: `gsap_animates_clip_element`.
3. **Body `font-family` must list concrete names**, not `var(--font-family)`. The static font analyzer doesn't expand CSS vars. Lint: `font_family_without_font_face`.
4. **No `Math.random()`, `Date.now()`, or network fetches** in composition scripts. Renders must be deterministic.
5. **Overlapping clips on the same `data-track-index`** = error. Give each element its own track index.
6. **The audio track lives on `data-track-index="10"`** by convention in these templates. Don't put other elements on 10.
7. **Fade-out tweens must land exactly on the `.set()` hard-kill,** not after it. Lint: `gsap_exit_missing_hard_kill`.
8. **No emoji in text**. The headless renderer doesn't paint color emoji reliably — use inline SVG or CSS shapes.
9. **Root `#stage`** must carry `data-composition-id`, `data-start`, `data-duration`, `data-fps`, `data-width`, `data-height`.
10. **Single paused GSAP timeline registered as `window.__timelines["<comp-id>"]`.** No auto-play, no `repeat: -1`.

---

## 10 · The standard editing loop

For every project, per edit:

```bash
cd videos/<my-project>
python3 assemble.py                                    # regenerate public/index.html
npx hyperframes lint public                             # 0 errors required
npx hyperframes snapshot public --at 2,8,15,22          # visual sanity check
PRODUCER_BROWSER_GPU_MODE=hardware \
  npx hyperframes render public --skill=<matching-skill> -o output.mp4 --fps 30
```

Render times on an M-series Mac: 60–90s for a 25–30s reel at 1080×1920.

---

## 11 · Quick reference — matching input to output

| The user hands you… | Archetype | Template | Skill flag |
|---|---|---|---|
| MP4 of one person speaking | 1 · talking-head | `templates/01-talking-head/` | `--skill=talking-head-recut` |
| A topic + a script (no footage) | 2 · faceless-explainer | `templates/02-faceless-explainer/` | `--skill=faceless-explainer` |
| Silent B-roll (spender vs saver, before/after) | 3 · split-broll | `templates/03-split-broll/` | `--skill=general-video` |
| "Make a cover for that reel" | 4 · cover | `templates/04-cover/` | `--skill=motion-graphics` |

---

## 12 · Instagram post copy conventions

Every Instagram caption ends with:

```
Prospur · AMFI-registered Mutual Fund Distributor · ARN-348873.
Mutual funds are subject to market risks; read all scheme-related documents carefully.
For information only, not investment advice.
```

Match this to whatever caption text the user drafts. Never post without the disclaimer in the caption AND the compliance strip on-screen.
