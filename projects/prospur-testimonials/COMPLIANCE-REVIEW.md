# Compliance review — 14 testimonial clips

**Nothing here is cleared for publishing.** These are customer testimonials
for an AMFI-registered Mutual Fund Distributor, and no one has yet confirmed
what the speakers actually say. Work through this before any of it goes out.

## Why you're doing this by ear

Automated transcription is not available in this environment. Every host
that serves a usable speech model is blocked by the network policy —
HuggingFace (whisper.cpp, faster-whisper, transformers), Azure
(openai-whisper), alphacephei (vosk), Zenodo, jsDelivr/unpkg, and GitHub
release assets all refuse. The one recognizer that ships its weights inside
a PyPI wheel and runs fully offline (pocketsphinx) was tested on this audio
and produces nonsense — a sample of clip 06 came back as *"i mean i found
his body to you on receiving them the city was in the mountains"*, and it
invents digits ("nine", "eight new") that aren't spoken. A screen built on
that would raise false alarms everywhere while still being capable of
missing a real return claim, which is the worst of both outcomes.

Source audio is not the problem — every segment sits at a clean −14 LUFS.
The recognizer is simply not good enough for accented, phone-recorded
conversational speech.

Worth noting regardless: a testimonial for a regulated entity needs a human
sign-off before publication anyway. A perfect transcript would have shortened
this review, not removed it.

## What disqualifies a clip

Mark a clip **NO** if the speaker does any of these:

- States or implies **returns, performance, or gains** — "I got 18%", "my
  money doubled", "I made ₹40,000", "better returns than FD"
- Names a **specific scheme or AMC**
- **Guarantees or promises** an outcome — "you'll definitely profit", "it's
  totally safe", "no risk"
- Gives **investment advice** — "you should put your money in X"

Mark **YES** only if the clip is purely about *experience* — service,
clarity, being helped to understand something, feeling looked after. That is
publishable; performance is not.

If a clip is 90% fine with one bad sentence, mark **TRIM** and note the
timecode — it can be cut around.

## The clips

Watch `public/testimonials-review.mp4` — same 14 clips, with the clip number
and timecode burned into the top-left corner so you always know what you're
listening to. Build it with `./build_review_cut.sh` if it isn't there.

| # | Timecode | Length | Who | Verdict | Notes |
|---|---|---|---|---|---|
| 01 | 0:00–1:10 | 70s | woman, seated indoors | | |
| 02 | 1:10–2:08 | 58s | woman, close-up | | |
| 03 | 2:08–2:22 | 15s | man, blue shirt, outdoors | | |
| 04 | 2:22–2:57 | 35s | woman, curly hair, glasses | | |
| 05 | 2:57–3:59 | 62s | woman, standing | | |
| 06 | 3:59–4:33 | 34s | woman, glasses, patterned wall | | |
| 07 | 4:33–5:59 | 86s | man, red Levi's tee, outdoors | | |
| 08 | 5:59–6:46 | 47s | woman, blue top | | |
| 09 | 6:46–7:32 | 46s | woman, glasses, sofa | | |
| 10 | 7:32–8:11 | 39s | woman, greenery background | | |
| 11 | 8:11–9:56 | 105s | woman, white top, bedroom | | |
| 12 | 9:56–10:45 | 49s | young man at table | | |
| 13 | 10:45–12:04 | 79s | **Aseem** (Adidas sweatshirt) | | |
| 14 | 12:04–13:14 | 69s | **Vedant** | | |

## After the review

Send back the list of cleared clip numbers (and any trim points). Turning
those into finished reels is then mechanical — reframing, brand treatment,
compliance strip and logo are all already built and proven in
`../prospur-saver-vs-spender/`.

Two things to decide at that point:

- **13:14 is not a Reels length.** Cleared clips most likely want to become
  either one short multi-speaker cut (a 5–8s soundbite each) or a set of
  individual per-speaker reels. That's a content call, not a technical one.
- **The compliance strip and caption disclaimer are still required** on
  whatever ships (PLAYBOOK.md §2 and §12), on top of clip-level clearance.
