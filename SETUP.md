# Setup Instructions

Copy everything in this folder into your `vinayak533/vinayak533` repo:

| File here | Goes to |
|---|---|
| `README.md` | repo root (replaces existing) |
| `assets/` | repo root — the four generated SVG panels |
| `tools/` | repo root — the generators |
| `.gitignore` | repo root |
| `.github/workflows/snake.yml` | same path |
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
| `assets/hero.svg` | `python tools/gen_hero.py` | Aurora banner: a drifting multi-colour gradient field with the **AI/ML ENGINEER** wordmark sweeping violet → cyan → magenta, over the one-line pitch. No name anywhere — the headline *is* the title. |
| `assets/about.svg` | `python tools/gen_about.py` | The About Me story as serif prose, fading up line by line. Edit `STORY` at the top of the script; `*asterisks*` mark the phrases that take the aurora gradient. |
| `assets/snake-dark.svg`<br />`assets/snake-light.svg` | `node tools/gen_snake.mjs` | Custom scattered snake (below), one file per theme. |

**The palette is the design.** Everything runs on one aurora ramp —
violet `#7C5CFF` → cyan `#22D3EE` → magenta `#F472B6` over near-black `#070b18`,
with indigo `#4F46E5` as the fourth blob. The hero wordmark, the `<em>` phrases in
the About prose, the snake's body and the repo-star badges all pull from that same
ramp, which is what keeps a page of unrelated third-party images reading as one design.
If you add anything new, colour it from that list.

**Both panels animate once, then stop.** The entrances use `both` fill and no
`infinite` — only the ambient layers (aurora drift, wordmark sweep, the snake) loop.
A header that re-runs its entrance every 20 seconds is the single most common thing
that makes a profile look cheap; don't reintroduce it.

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
  — cyan → indigo → violet → magenta.
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

- **Hero pitch**: the one-liner under the wordmark is `PITCH` in `tools/gen_hero.py`.
  It is the single most-read string on the profile — it should say what you build and
  who it is for, not list technologies.
- **Hero motion**: `BLOBS` controls the aurora — each entry is
  `(cx, cy, rx, ry, colour, drift-x, drift-y, seconds)`. The durations are deliberately
  co-prime-ish (23/26/29/31/37s) so the field never visibly repeats.
- **About stagger**: `STEP` is the delay between lines; `PROSE_WRAP` the line length.

## Adding a languages row back

The stack is deliberately short, but recruiters and ATS keyword-filters screen on
language names before a human ever sees the page. `Python` is in there for exactly
that reason. To add the rest, drop this above the GenAI row in `README.md`:

```html
<p align="center">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
</p>
```
