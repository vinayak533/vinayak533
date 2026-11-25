# Profile design & maintenance

The README is the profile. Every panel is a generated SVG; the only scheduled data component is the contribution panel.

## Design system

- **Idea** — the headline is "AI systems that show their work", so each project card is an animated film of its system working.
- **Stage** — one black surface, the same as behind the hero butterfly, in both GitHub themes: 24 px radius, one hairline border, 36 px desktop / 24 px compact padding. Two cards leave it on purpose: the research paper is an ivory journal page, and the portfolio uses the site's own blue (`#2261E9`) with Neo.
- **Films** (`scenes.py`) — every element stores its on/off time in seconds on one shared loop. A negative delay starts playback on the finished frame, so first paint, reduced motion and non-animating viewers see the completed state. loom.ai replays the repository's scripted demo turn and races 8.9 s against 5.0 s in real seconds; lazyhire filters fixture listings and rejects an untraceable CV line; InForge-AI loses its LLM provider and still finishes.
- **Paper figures** are schematic: a linear SVM boundary, a random-forest vote and a logistic curve. They plot no study data.
- **Colour carries meaning** — blue = agent systems (loom.ai), green = grounded generation (lazyhire), amber = applied ML (InForge-AI), violet = the butterfly, activity and contact.
- **Type** — the visitor's system sans, Georgia italic for the hero's rolling line and Georgia for the paper. No embedded fonts. Sentence case.
- **Motion** — hero butterfly flight and rolling headline (14 s), proof-band digits that roll once, project films (13–15 s), paper figures (11 s), Neo's float, head tilt, blink and speech, a beam of light around each project card, ripples through the expertise icons and activity columns, and drifting contact lights. Reduced motion stops all of it.
- **Responsive** — each panel has an 880 px desktop and a 400 px compact variant, chosen by `<picture>` media queries: compact below 640 px and between 768–959 px (where GitHub's profile sidebar narrows the README column).

## Files

| Path | Purpose |
| --- | --- |
| `README.md` | Hero → introduction → proof → selected work → research → portfolio → more projects → expertise → stack → activity → contact |
| `tools/profile/theme.py` | Tokens, surfaces, glyphs, dot-matrix icons |
| `tools/profile/scenes.py` | Film clock and the three project films |
| `tools/profile/pages.py` | Research paper and portfolio cards |
| `tools/profile/build.py` | Hero, proof band, expertise, stack, contact, link buttons; writes every panel |
| `tools/profile/activity.py` | Validated contribution data and the dot-matrix activity panel |
| `scripts/generate_butterfly.py` | Stippled, animated butterfly: writes `assets/butterfly.svg` and supplies the same art to the hero (README images can't load other files, so it is inlined) |
| `assets/svg/` | Generated: desktop + compact variants and link buttons. The `*-dark*.svg` files belong to the previous design and are no longer used or rebuilt |
| `assets/screens/` | Real project screenshots, unchanged; `web/` holds the Neo cutout embedded in the portfolio card |
| `.github/workflows/activity.yml` | Daily refresh of the activity variants |

## Regenerate

```bash
python tools/profile/build.py
python tools/profile/activity.py
python scripts/generate_butterfly.py   # standalone assets/butterfly.svg; build.py already inlines it in the hero
```

Both use only the standard library. `build.py` needs no network; the butterfly artwork is seeded, so rebuilds are byte-stable. `activity.py` uses `GITHUB_TOKEN` when present, otherwise GitHub's public contribution calendar; `GH_LOGIN` defaults to `vinayak533`. It checks date continuity, range, levels and totals before writing, and keeps the existing panel if anything fails. The workflow needs `contents: write` to commit refreshed panels; neither script pushes.

The portfolio cards embed `assets/screens/web/neo.webp` (base64, ~38 KB), a transparent cutout of the robot from vinayakkv.com.

## Content rules

- Every claim traces to a public repository README or the original profile: 8 models across Groq, OpenRouter and OpenCode; ten specialist agents; median time-to-first-token 8.9 s → 5.0 s (loom.ai `docs/performance.md`); nine Kerala sources and zero-fabrication CV guardrails (lazyhire); local fallbacks when LLM calls fail (InForge-AI). Employment, location and credentials come from the original profile.
- The proof band: 44% is (8.9 − 5.0) / 8.9 from loom.ai's `docs/performance.md`; 10 agents from its README; 18/20 from NL2SQL's own benchmark; the paper is Zenodo DOI 10.5281/zenodo.20253956.
- The principles row (deterministic core, cite or abstain, fail over not out, documented limits) restates the original profile's principles section.
- Screenshot captions keep their scripted / seeded / fixture qualifications.
- The stack lists only technologies declared in the featured projects' dependency files.
- The activity panel is drawn only from real GitHub data — never decorative cells.

## Review after edits

1. Rebuild, then check every SVG's text stays inside its viewBox without collisions.
2. Render the README on both GitHub page colours (dark and white) at 360, 390, 639, 640, 767, 768, 959, 960 and 1280 px inside a profile-like layout (sidebar from 768 px).
3. Check source selection, image loads, link targets, and horizontal overflow with disclosures open.
4. Check reduced motion: no CSS animation runs, motion-only layers are hidden, and all content remains.

Local `preview-*.html`, `.preview-output/`, browser binaries and preview dependencies are ignored by Git. Final hosted appearance depends on GitHub's renderer and image cache. GitHub documents the [`picture` element](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#the-picture-element) and [theme-aware images](https://github.blog/developer-skills/github/how-to-make-your-images-in-markdown-on-github-adjust-for-dark-mode-and-light-mode/).
