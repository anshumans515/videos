# remotion-prospur

A **Remotion** scaffold for Prospur reels, pinned to Remotion `4.0.505` exact.
This is deliberately empty — the toolchain, brand tokens, and reel format are
wired up; the reels themselves are not built here yet.

> Note: this is a *separate* toolchain from the rest of this repo. The shipped
> reels (`projects/prospur-saver-vs-spender`, `projects/prospur-cover`) are
> built with **HyperFrames** (Python `assemble.py` → HTML+GSAP), not Remotion.
> Nothing here replaces those. This is a parallel setup for building reels in
> React instead.

## Prerequisites

- Node.js 18+ and `ffmpeg` on PATH — `node -v && ffmpeg -version`
- On a fresh Mac: `brew install node ffmpeg`

## Setup

```bash
cd remotion-prospur
npm install          # installs the exact pinned versions from package.json
```

## Use

```bash
npm run studio          # live preview at http://localhost:3000
npm run compositions    # list registered compositions
npm run render Empty out/empty.mp4
npm run typecheck
```

`remotion studio` is the "Remotion features" — hot-reloading preview, a
timeline you can scrub, and props editing. It opens whatever is registered in
`src/Root.tsx`.

## Layout

```
src/
  index.ts        registerRoot entry point (keep tiny)
  Root.tsx        registers every <Composition> — add reels here
  Empty.tsx       placeholder comp (brand-ground frame, nothing else)
  brand.ts        Prospur tokens + the 1080x1920 / 30fps reel format
remotion.config.ts  render defaults
tsconfig.json
```

To add a reel: build a component under `src/`, then register it in
`Root.tsx` with `<Composition id="…" component={…} durationInFrames={…}
{...REEL} />`.

## Chrome note (only matters in restricted networks)

Remotion renders through its own Chrome Headless Shell, which it downloads on
first render from `remotion.media`. On a normal machine this just works. In a
sandbox with an egress allowlist that download 403s — point Remotion at an
existing Chromium instead:

```bash
npm run render Empty out/empty.mp4 -- --browser-executable=/path/to/chrome
```

(In this repo's sandbox that path is
`/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`,
which is how this scaffold was verified — a 15-frame render of `Empty`
produced a valid 1080x1920/30fps MP4.)

## Versions (pinned exact)

| package | version |
|---|---|
| remotion | 4.0.505 |
| @remotion/cli | 4.0.505 |
| react / react-dom | 19.2.8 |
| typescript | 5.7.3 |

`package.json` pins these with no `^`, so `npm install` reproduces the exact
toolchain on any machine.
