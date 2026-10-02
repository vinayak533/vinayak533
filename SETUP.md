# Profile setup

Everything visual in the README is generated. Edit the generator, re-run it, and commit the output.

## Layout

| Path | What it is |
|---|---|
| `README.md` | The profile. Each visual is a `<picture>` with a dark and a light SVG. |
| `assets/svg/` | Generated panels: `{name}-dark.svg` and `{name}-light.svg`. |
| `assets/screens/` | Real screenshots from loom.ai and lazyhire, framed at 1440×900. |
| `tools/profile/theme.py` | Design tokens (colors, fonts, mobile breakpoint) and SVG helpers. |
| `tools/profile/build.py` | Hero, status, console, system map, cards, architecture, stack, dividers, footer. |
| `tools/profile/activity.py` | Contribution panel from live GitHub data. |
| `.github/workflows/activity.yml` | Re-renders the contribution panel daily at 02:17 UTC. |

## Regenerate

```bash
python tools/profile/build.py      # static panels, no network
python tools/profile/activity.py   # contribution panel; uses GITHUB_TOKEN if set, else the public calendar page
```

Neither script has dependencies beyond the Python standard library. `activity.py` exits without
writing if it can't fetch a full year of data, so it never commits a made-up grid.

## Design rules

- **One accent.** Google blue (`#8AB4F8` dark / `#1A73E8` light) for structure; amber only for live or streaming states.
- **Two layouts per panel.** Each SVG has a `.dsk` and a `.mob` group, switched by a media query inside the SVG,
  which evaluates against the width the image is drawn at. Below 560 px (phones) panels switch to larger type
  and shorter labels. Test both when you change copy.
- **Animate once, then idle.** Entrances use `both` fill and run once; only slow ambient motion loops.
  `prefers-reduced-motion` disables the CSS animations.
- **System fonts only.** GitHub serves SVGs as images, which can't load web fonts.
- **Evidence over adjectives.** Every capability on the system map and every focus line in the console names
  the repository that implements it. Keep it that way when adding entries.

## Editing copy

| To change | Edit |
|---|---|
| Hero name, identity line, statement | `hero()` in `build.py` |
| Status cells | `status()`: `cells` (desktop) and `mob` (phone) |
| Console lines | `terminal()`: `desk` / `mob` lists and `focus` |
| System map | `MAP` |
| Project cards | `CARDS` (desktop lines max about 23 characters per flow box) |
| Stack | `STACK`: only add technologies a featured repo actually depends on |

## Preview locally

```bash
python -m http.server 8777
```

Open any `preview*.html` you create in the repo root (they're gitignored), or open an SVG directly.
Chrome only runs SVG-image animations that are on screen, so scroll to see each entrance.

## One-time GitHub settings

**Settings → Actions → General → Workflow permissions → Read and write**, so the activity workflow can commit.
