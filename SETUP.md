# Setup Instructions

Copy everything in this folder into your `vinayak533/vinayak533` repo:

| File here | Goes to |
|---|---|
| `README.md` | repo root (replaces existing) |
| `assets/` | repo root — the four generated SVG panels |
| `tools/` | repo root — the generators |
| `.gitignore` | repo root |
| `.github/workflows/snake.yml` | same path |
| `.github/workflows/profile-3d-contrib.yml` | same path |
| `.github/workflows/metrics.yml` | same path |

`preview.html` is only for local previewing — it's gitignored, don't copy it.

## 1. Enable Actions write access
Repo → **Settings → Actions → General → Workflow permissions** → **Read and write permissions** → Save.

## 2. Token for the metrics action
`lowlighter/metrics` works best with a personal access token. The workflow falls back
to the built-in `GITHUB_TOKEN` if `METRICS_TOKEN` is missing, so it still runs either
way — but some plugins produce less without a PAT.

1. https://github.com/settings/tokens → **Generate new token (classic)**
2. Scope: **`public_repo`** only.
3. Repo → **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `METRICS_TOKEN`, Value: the token

The snake and 3D-graph workflows need no extra token.

## 3. Push and run
Push, then in the **Actions** tab run each workflow once with **Run workflow**. Until
`profile-3d-contrib/profile-season-animate.svg` and `github-metrics.svg` exist, those two
sections show broken images — expected.

---

## The generated panels

Everything visual lives in `assets/` and is produced by scripts in `tools/`. Regenerate
locally, then commit the SVG.

| Panel | Command | Notes |
|---|---|---|
| `assets/hero.svg` | `python tools/gen_hero.py` | Full-width terminal: types a short program, runs it, and prints **AI/ML ENGINEER** as the program's own stdout. No name anywhere — the headline *is* the title. |
| `assets/about.svg` | `python tools/gen_about.py` | The About Me story told twice: first typed out as `about.html`, then "rendered" as serif prose. Edit `STORY` at the top of the script — it feeds **both** halves, so they cannot drift. `*asterisks*` become `<em>` in the markup and the accent colour in the prose. |
| `assets/snake-dark.svg`<br />`assets/snake-light.svg` | `node tools/gen_snake.mjs` | Custom scattered snake (below), one file per theme. |

The whole design runs on one accent colour (`#4FD1E0`) over deep navy (`#05091a`),
with hairline rules instead of glows. There are deliberately no blur/glow filters in
any panel — if you add one, it will stand out badly against the rest.

Preview them without pushing:

```bash
python -m http.server 8777
```

then open `http://127.0.0.1:8777/preview.html` — each panel has a scrubber so you can
step through its animation timeline.

## The scattered snake

`Platane/snk` walks the contribution grid line by line. `tools/gen_snake.mjs` replaces it:

- **Scattered route.** It picks one of the three nearest uneaten contribution cells at
  random, and every 14th hop deliberately dashes to the far side of the board. Moves are
  L-shaped or staircase, so the path reads as a hunt rather than a sweep.
- **Colour burst on contact.** Each cell that gets eaten fires a soft bloom and a thin
  expanding shockwave ring, keyed to that day's contribution level
  — cyan → green → indigo → mauve.
- **Slow, clean pacing.** Tempo is set by `SEC_PER_STEP` (0.075s per cell) and clamped to a
  40–80s loop, on a GitHub-style calendar with month and weekday labels.
- **Seamless loop.** The route closes back on its start, so the snake wraps without a jump.

The workflow (`snake.yml`) runs daily at 02:17 UTC and commits both themes. The README
picks between them with a `<picture>` element, so the panel follows the reader's
GitHub light/dark setting.

**The checked-in snake is synthetic placeholder data.** Without a `GITHUB_TOKEN` the
generator invents a grid so you can preview the motion locally, so the committed file
shows an invented year until the workflow has run once against the real API.

Run it locally against real data:

```bash
GH_LOGIN=vinayak533 GITHUB_TOKEN=ghp_xxx node tools/gen_snake.mjs
```

Without a token it generates a synthetic grid so you can still preview the motion.

Knobs at the top of the script: `CELL` / `GAP` / `PAD` for geometry, `THEMES` for the
grid palette, `BURST` for the per-level hit colours. Routing lives in `buildRoute()` —
`hop % 14` controls how often it takes a long dash, `Math.min(3, …)` how random the
short hops are.

## Services used by the README

These are third-party image endpoints, so they can rate-limit or go down:

| Service | Used for | Status when this was written |
|---|---|---|
| `skillicons.dev` | tech stack icons | ✅ |
| `img.shields.io` | badges, repo stars | ✅ |
| `github-readme-activity-graph.vercel.app` | commit-over-time chart | ✅ |
| `github-profile-summary-cards.vercel.app` | profile details, languages, productive time | ✅ |
| `streak-stats.demolab.com` | streak card | ✅ |
| `capsule-render.vercel.app` | footer wave | ✅ |

Deliberately **not** used: `github-readme-stats.vercel.app` and
`github-profile-trophy.vercel.app` — both were returning 503 / 402 and would have
rendered as broken images.

## Optional tweaks

- **3D graph style**: the action writes several variants into `profile-3d-contrib/`. The
  README uses `profile-season-animate.svg`; `profile-night-rainbow.svg`,
  `profile-night-view.svg` and `profile-gitblock.svg` are also generated. There is no
  `profile-custom.svg` — that needs a `SETTING_JSON` file, which this setup doesn't use.
- **Hero code**: the lines shown on screen are the `LINES` list in `tools/gen_hero.py`.
- **Hero timing**: `LOOP`, `TYPE_SLOTS`, `BOX_A/B`, `CHAR_A`, `HOLD_B` control the pacing.
- **About timing**: `TYPE_A/B` is the code-typing window, `CODE_OUT_A/B` the hand-off,
  `PROSE_A` / `PROSE_STEP` how the sentences stagger in.
