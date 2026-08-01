# Fonts

Per PLAYBOOK.md §1: both typefaces are bundled here and **never** fetched
from a network at render time (HyperFrames lint blocks external `src=` URLs
in composition scripts, and even non-blocked CDN fetches are unreliable in
the headless render).

This directory should contain the actual font binaries, which are not
checked into this scaffold (license files, not source — drop your own
licensed copies in):

```
assets/fonts/
  Inter-Regular.woff2      (weight 400)
  Inter-Bold.woff2         (weight 700)
  SourceSerif4-Medium.woff2   (weight 500)
  SourceSerif4-SemiBold.woff2 (weight 600)
```

Both are open-source (Inter: OFL, Source Serif 4: OFL) and can be obtained
from their respective GitHub release pages — just don't `fetch()` them at
render time.

`fonts.css` below declares concrete `font-family` names so it satisfies
HyperFrames lint rule `font_family_without_font_face` (PLAYBOOK.md §9.3):
composition CSS must reference `'Inter'` / `'Source Serif 4'` directly, never
a CSS custom property.

Include it in a template's `<head>` with a relative `<link>` (or inline the
`@font-face` blocks directly into the composition — see
`templates/01-talking-head/assemble.py` for the pattern each template uses).
