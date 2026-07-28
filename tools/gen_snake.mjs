#!/usr/bin/env node
/**
 * Scattered contribution snake.
 *
 * Platane/snk sweeps the grid line by line. This one hunts: it repeatedly darts
 * to a nearby (and every so often, a far) contribution cell, so the route reads
 * as scattered rather than as a lawnmower. Every cell it eats pops with a colour
 * burst keyed to that day's contribution level.
 *
 *   GH_LOGIN=vinayak533 GITHUB_TOKEN=xxx node tools/gen_snake.mjs
 *
 * With no token it falls back to synthetic data so you can preview locally.
 *
 * Writes one file per entry in THEMES -> assets/snake-{dark,light}.svg, both off
 * the same route so the two panels stay in step.
 *
 * Size trick: all of the per-cell effects share a handful of @keyframes and are
 * offset purely with `animation-delay`, so 300+ animated cells cost ~200 bytes
 * each instead of ~1 KB of SMIL.
 */

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, "..");

const LOGIN = process.env.GH_LOGIN || "vinayak533";
const TOKEN = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || "";

// ------------------------------------------------------------------ geometry
const CELL = 14;
const GAP = 3;
const PITCH = CELL + GAP;
const LEFT = 32;   // gutter for the weekday labels
const TOP = 24;    // strip for the month labels
const EDGE = 16;   // right / bottom margin
const ROWS = 7;

// how long the snake dwells on each cell, in seconds — the pacing dial
const SEC_PER_STEP = 0.075;
const MIN_LOOP = 40;
const MAX_LOOP = 80;

// how long each hit effect lasts, in seconds (independent of the loop length)
const FX = { drain: 0.45, ring: 1.0, bloom: 0.55 };

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const WEEKDAYS = { 1: "Mon", 3: "Wed", 5: "Fri" };

// ------------------------------------------------------------------ palettes
const THEMES = {
  dark: {
    cells: ["#131a2b", "#173a45", "#1d6272", "#2b93a6", "#4FD1E0"],
    snake: ["#3d6d9e", "#3aa3bb", "#4FD1E0"],
    label: "#5d6b85",
    caption: "#39445c",
  },
  light: {
    cells: ["#eef1f6", "#cfe6ec", "#9fcfda", "#5aa8bd", "#2b7c92"],
    snake: ["#4a7fb5", "#3f9cb5", "#2fb4c8"],
    label: "#7b8798",
    caption: "#98a3b3",
  },
};

// one colour per contribution level, so a busy day bursts differently to a quiet one
const BURST = ["#4FD1E0", "#4FD1E0", "#5FBF9A", "#8AA0E0", "#C88AC0"];

const LEVEL = {
  NONE: 0,
  FIRST_QUARTILE: 1,
  SECOND_QUARTILE: 2,
  THIRD_QUARTILE: 3,
  FOURTH_QUARTILE: 4,
};

// ------------------------------------------------------------------ data
async function fetchGrid() {
  if (!TOKEN) {
    console.warn("! no GITHUB_TOKEN - generating synthetic grid for preview");
    return synthetic();
  }
  const query = `query($login:String!){
    user(login:$login){ contributionsCollection{ contributionCalendar{
      weeks{ contributionDays{ contributionCount contributionLevel weekday date } } } } }
  }`;
  const res = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `bearer ${TOKEN}`,
      "Content-Type": "application/json",
      "User-Agent": "scattered-snake",
    },
    body: JSON.stringify({ query, variables: { login: LOGIN } }),
  });
  if (!res.ok) throw new Error(`GitHub API ${res.status}: ${await res.text()}`);
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));

  const weeks = json.data.user.contributionsCollection.contributionCalendar.weeks;
  return weeks.map((w) => {
    const col = new Array(ROWS).fill(null);
    for (const d of w.contributionDays) {
      col[d.weekday] = {
        level: LEVEL[d.contributionLevel] ?? 0,
        count: d.contributionCount,
        date: d.date,
      };
    }
    return col;
  });
}

function synthetic() {
  let seed = 7;
  const rnd = () => ((seed = (seed * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff);
  const end = new Date();
  end.setDate(end.getDate() - end.getDay()); // back to a Sunday
  return Array.from({ length: 53 }, (_, w) =>
    Array.from({ length: ROWS }, (_, d) => {
      const day = new Date(end);
      day.setDate(day.getDate() - (52 - w) * 7 + d);
      const r = rnd();
      const level = r < 0.55 ? 0 : r < 0.74 ? 1 : r < 0.87 ? 2 : r < 0.96 ? 3 : 4;
      return { level, count: level * 3, date: day.toISOString().slice(0, 10) };
    })
  );
}

// ------------------------------------------------------------------ routing
function makeRng(seed) {
  let s = seed >>> 0;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >> 17;
    s ^= s << 5; s >>>= 0;
    return s / 0xffffffff;
  };
}

/** one grid step at a time from `a` to `b`; `mode` shapes the dash */
function walk(a, b, mode, push) {
  let { x, y } = a;
  if (mode === "stair") {
    // alternate axes -> reads as a diagonal dart across the board
    while (x !== b.x || y !== b.y) {
      if (x !== b.x) { x += Math.sign(b.x - x); push({ x, y }); }
      if (y !== b.y) { y += Math.sign(b.y - y); push({ x, y }); }
    }
    return;
  }
  const first = mode === "yx" ? "y" : "x";
  for (const axis of [first, first === "x" ? "y" : "x"]) {
    if (axis === "x") while (x !== b.x) { x += Math.sign(b.x - x); push({ x, y }); }
    else while (y !== b.y) { y += Math.sign(b.y - y); push({ x, y }); }
  }
}

function buildRoute(cols) {
  const rnd = makeRng(0x5eed1234);
  const food = [];
  cols.forEach((col, x) =>
    col.forEach((d, y) => {
      if (d && d.level > 0) food.push({ x, y, level: d.level });
    })
  );
  if (!food.length) food.push({ x: 0, y: 3, level: 1 });

  const start = { x: 0, y: 0 };
  const route = [start];
  const eaten = [];
  const push = (p) => route.push(p);

  let cur = start;
  let hop = 0;
  const remaining = food.slice();

  while (remaining.length) {
    // rank by distance, then pick among the closest few -> wandering, not sweeping
    const scored = remaining
      .map((f, i) => ({ i, d: Math.abs(f.x - cur.x) + Math.abs(f.y - cur.y) }))
      .sort((a, b) => a.d - b.d);

    let pickIdx;
    if (hop % 14 === 13 && scored.length > 20) {
      // now and then, a long dash to the far side of the board
      const far = scored.slice(Math.floor(scored.length * 0.6));
      pickIdx = far[Math.floor(rnd() * far.length)].i;
    } else {
      const k = Math.min(3, scored.length);
      pickIdx = scored[Math.floor(rnd() * k)].i;
    }

    const target = remaining.splice(pickIdx, 1)[0];
    const r = rnd();
    walk(cur, target, r < 0.34 ? "stair" : r < 0.67 ? "xy" : "yx", push);
    eaten.push({ x: target.x, y: target.y, level: target.level, step: route.length - 1 });
    cur = target;
    hop++;
  }

  // close the loop so the animation can wrap seamlessly
  walk(cur, start, "xy", push);
  return { route, eaten };
}

// ------------------------------------------------------------------ svg
const cx = (x) => LEFT + x * PITCH + CELL / 2;
const cy = (y) => TOP + y * PITCH + CELL / 2;

function css(t, dur) {
  // effect windows are authored in seconds, then converted -> same feel at any tempo
  const p = (sec) => `${((sec / dur) * 100).toFixed(3)}%`;
  const lv = t.cells.map((c, i) => `.l${i}{fill:${c}}`).join("");
  const bs = BURST.map((c, i) => `.b${i}{stroke:${c};fill:${c}}`).join("");

  return (
    "<style>" +
    lv +
    bs +
    `.eat{animation:eat ${dur}s linear infinite}` +
    `@keyframes eat{0%{opacity:1}${p(FX.drain)}{opacity:.15}99.3%{opacity:.15}100%{opacity:1}}` +
    // a single thin shockwave — the colour carries the level, so one ring is enough
    `.r{fill:none;stroke-width:2.2;animation:ring ${dur}s linear infinite}` +
    `@keyframes ring{0%{r:5;opacity:.85;stroke-width:2.4}` +
    `${p(FX.ring)}{r:23;opacity:0;stroke-width:.5}` +
    `${p(FX.ring + 0.02)},100%{r:0;opacity:0}}` +
    `.bl{animation:bloom ${dur}s linear infinite}` +
    `@keyframes bloom{0%{r:10;opacity:.5}${p(FX.bloom)}{r:3;opacity:0}` +
    `${p(FX.bloom + 0.02)},100%{r:0;opacity:0}}` +
    "</style>"
  );
}

/** month name for each column that starts a new month, GitHub-style */
function monthLabels(cols) {
  const out = [];
  let last = -1;
  cols.forEach((col, x) => {
    const first = col.find((d) => d && d.date);
    if (!first) return;
    const m = new Date(first.date + "T00:00:00Z").getUTCMonth();
    if (m !== last && x < cols.length - 1) {
      // skip a label that would sit right on top of the previous one
      if (!out.length || x - out[out.length - 1].x >= 3) out.push({ x, m });
      last = m;
    }
  });
  return out;
}

function render(cols, route, eaten, theme, dur) {
  const t = THEMES[theme];
  const W = LEFT + cols.length * PITCH - GAP + EDGE;
  const H = TOP + ROWS * PITCH - GAP + 24;
  const N = route.length;
  const delay = (step) => ((step / (N - 1)) * dur).toFixed(2);

  const d = "M" + route.map((p) => `${cx(p.x)},${cy(p.y)}`).join("L");

  const out = [];
  out.push(
    `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" ` +
      `width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" ` +
      `role="img" aria-label="${LOGIN} contribution grid being eaten by a snake">`
  );

  out.push("<defs>");
  out.push(
    `<linearGradient id="sn" x1="0" y1="0" x2="1" y2="1">` +
      t.snake
        .map((c, i) => `<stop offset="${(i / (t.snake.length - 1)) * 100}%" stop-color="${c}"/>`)
        .join("") +
      `</linearGradient>`
  );
  out.push(`<path id="route" d="${d}" fill="none"/>`);
  out.push("</defs>");
  out.push(css(t, dur));

  // ---- calendar labels
  const lab = [];
  const FONT = "ui-monospace,SFMono-Regular,Consolas,monospace";
  for (const { x, m } of monthLabels(cols)) {
    lab.push(
      `<text x="${LEFT + x * PITCH}" y="${TOP - 9}" font-family="${FONT}" font-size="10" ` +
        `fill="${t.label}">${MONTHS[m]}</text>`
    );
  }
  for (const [row, name] of Object.entries(WEEKDAYS)) {
    lab.push(
      `<text x="${LEFT - 8}" y="${cy(+row) + 3.5}" font-family="${FONT}" font-size="10" ` +
        `fill="${t.label}" text-anchor="end">${name}</text>`
    );
  }
  out.push(`<g>${lab.join("")}</g>`);

  // ---- grid
  const hits = new Map(eaten.map((e) => [`${e.x},${e.y}`, e]));
  const cells = [];
  const blooms = [];
  const rings = [];

  cols.forEach((col, x) =>
    col.forEach((day, y) => {
      if (!day) return;
      const X = LEFT + x * PITCH;
      const Y = TOP + y * PITCH;
      const hit = hits.get(`${x},${y}`);

      if (!hit) {
        cells.push(`<rect class="l${day.level}" x="${X}" y="${Y}" width="${CELL}" height="${CELL}" rx="3"/>`);
        return;
      }
      const dl = delay(hit.step);
      cells.push(
        `<rect class="l${day.level} eat" x="${X}" y="${Y}" width="${CELL}" height="${CELL}" rx="3" ` +
          `style="animation-delay:${dl}s"/>`
      );
      blooms.push(
        `<circle class="bl b${day.level}" cx="${cx(x)}" cy="${cy(y)}" r="0" opacity="0" ` +
          `style="animation-delay:${dl}s"/>`
      );
      rings.push(
        `<circle class="r b${day.level}" cx="${cx(x)}" cy="${cy(y)}" r="0" opacity="0" ` +
          `style="animation-delay:${dl}s"/>`
      );
    })
  );

  out.push(`<g>${cells.join("")}</g>`);
  out.push(`<g>${blooms.join("")}</g>`);

  // ---- snake: every segment rides one shared path, offset by a step
  const SEGS = 7;
  const step = 1 / (N - 1);
  const snake = [];
  for (let j = SEGS - 1; j >= 0; j--) {
    const s = j * step;
    const size = CELL - 1.5 - j * 0.8;
    const op = (1 - j * 0.07).toFixed(2);
    const kp = j === 0 ? "0;1" : `${(1 - s).toFixed(6)};1;0;${(1 - s).toFixed(6)}`;
    const kt = j === 0 ? "0;1" : `0;${s.toFixed(6)};${s.toFixed(6)};1`;
    snake.push(
      `<g><rect x="${(-size / 2).toFixed(2)}" y="${(-size / 2).toFixed(2)}" width="${size.toFixed(2)}" ` +
        `height="${size.toFixed(2)}" rx="${(size / 3).toFixed(2)}" fill="url(#sn)" opacity="${op}"/>` +
        `<animateMotion dur="${dur}s" repeatCount="indefinite" calcMode="linear" ` +
        `keyPoints="${kp}" keyTimes="${kt}">` +
        `<mpath href="#route" xlink:href="#route"/></animateMotion></g>`
    );
  }
  out.push(`<g>${snake.join("")}</g>`);
  out.push(`<g>${rings.join("")}</g>`);

  out.push(
    `<text x="${LEFT}" y="${H - 5}" font-family="${FONT}" font-size="10" fill="${t.caption}">` +
      `${eaten.length} contribution days · scattered hunt · ${dur}s loop</text>`
  );
  out.push("</svg>");
  return out.join("");
}

// ------------------------------------------------------------------ main
const cols = await fetchGrid();
const { route, eaten } = buildRoute(cols);

const dur = Math.round(
  Math.min(MAX_LOOP, Math.max(MIN_LOOP, route.length * SEC_PER_STEP))
);

mkdirSync(resolve(ROOT, "assets"), { recursive: true });
for (const theme of Object.keys(THEMES)) {
  const svg = render(cols, route, eaten, theme, dur);
  const file = resolve(ROOT, "assets", `snake-${theme}.svg`);
  writeFileSync(file, svg, "utf8");
  console.log(`wrote ${file}  (${(svg.length / 1024).toFixed(1)} KB)`);
}
console.log(
  `route ${route.length} steps · ${eaten.length} cells eaten · ${dur}s loop ` +
    `(${(dur / route.length).toFixed(3)}s per cell)`
);
