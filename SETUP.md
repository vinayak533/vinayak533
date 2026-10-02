# Profile design & maintenance

The README is the profile. Every panel is a generated SVG; the only scheduled data component is the contribution panel.

## Design system

- **Surfaces** — dark glass cards lit from below: a tinted body, a bloom rising from the bottom edge, and a rim that brightens toward the light. The profile publishes this dark art in both GitHub colour modes (`PUBLISHED` in `theme.py`; a light palette is kept there but not built). Anything that sits directly on the page — link pills, the principles strip — has an opaque dark base so it reads on white too. 20 px card radius, fully rounded pills, 36 px desktop / 24 px compact padding.
- **Colour carries meaning** — blue = agent systems (loom.ai), green = grounded generation (lazyhire), orange = applied ML (InForge-AI). The expertise trio and the project cards share this mapping. Other hues appear only inside pills (agent-loop steps, stack categories, link buttons). Green dots mean availability.
- **Pills** — tinted fill, gradient border, filled icon disc.
- **Dot matrix** — the hero butterfly (thousands of blue-noise stippled dots, dense and white at the body, sparse with violet margins at the wing edges) and the activity panel (one column per week; lit cells proportional to that week's real total).
- **Type** — GitHub's system sans and mono stacks, with one italic serif accent per headline (Georgia stack). No embedded fonts.
- **Motion** — slow and optional: name sheen, butterfly wing flap (2.4 s), float, dot twinkle and violet particles shed on each wingbeat, agent-loop steps lighting in sequence, the loom.ai request pulse and event flow, availability pings. CSS honours `prefers-reduced-motion` and motion-only layers are hidden. Every panel is complete on its first frame.
- **Responsive** — each panel has a 880 px desktop and a 400 px compact variant, chosen by `<picture>` media queries: compact below 640 px and between 768–959 px (where GitHub's profile sidebar narrows the README column). Art renders between 0.65× and 1.45× at every width.

## Files

| Path | Purpose |
| --- | --- |
| `README.md` | Hero → introduction → expertise → selected work → activity → stack → contact |
| `tools/profile/theme.py` | Tokens, hue palette, glass/glow surfaces, glyphs, pills |
| `tools/profile/build.py` | Hero, expertise, project cards, framed screenshot, stack, contact, link pills |
| `tools/profile/activity.py` | Validated contribution data and the dot-matrix activity panel |
| `scripts/generate_butterfly.py` | Stippled, animated butterfly: writes `assets/butterfly.svg` and supplies the same art to the hero (README images can't load other files, so it is inlined) |
| `assets/svg/` | Generated: desktop + compact variants, link pills and the framed screenshot (dark) |
| `assets/screens/` | Real project screenshots, unchanged |
| `.github/workflows/activity.yml` | Daily refresh of the activity variants |

## Regenerate

```bash
python tools/profile/build.py
python tools/profile/activity.py
python scripts/generate_butterfly.py   # standalone assets/butterfly.svg; build.py already inlines it in the hero
```

Both use only the standard library. `build.py` needs no network; the butterfly artwork is seeded, so rebuilds are byte-stable. `activity.py` uses `GITHUB_TOKEN` when present, otherwise GitHub's public contribution calendar; `GH_LOGIN` defaults to `vinayak533`. It checks date continuity, range, levels and totals before writing, and keeps the existing panel if anything fails. The workflow needs `contents: write` to commit refreshed panels; neither script pushes.

`screen-loom-*.svg` embeds `assets/screens/loom-agent-trace.png` (base64) inside a window frame, so it is ~390 KB. Rebuild after replacing that screenshot.

## Content rules

- Every claim traces to a public repository README or the original profile: 8 models across Groq, OpenRouter and OpenCode; ten specialist agents; median time-to-first-token 8.9 s → 5.0 s (loom.ai `docs/performance.md`); nine Kerala sources and zero-fabrication CV guardrails (lazyhire); local fallbacks when LLM calls fail (InForge-AI). Employment, location and credentials come from the original profile.
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
