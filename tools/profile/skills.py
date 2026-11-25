"""Technical skills panel: original logos on white tiles, plus drawn symbols for concepts that have no logo."""
import base64
from pathlib import Path

from theme import V, W, MW, P, MP, doc, hline, surface, text

ICONS = Path(__file__).resolve().parents[2] / "assets/icons"

# (label lines, logo file or drawn symbol)
SKILLS = [
    ("Languages", [("Python", "python.svg"), ("TypeScript", "typescript.svg"), ("SQL", "*sql"), ("C++", "cplusplus.svg")]),
    ("AI & Agents", [("LangGraph", "langgraph.svg"), ("LangChain", "langchain.svg"), ("Multi-Agent Systems", "*agents"), ("RAG", "*rag"),
                     ("Tool Calling", "*tool"), ("LLM Routing", "*route"), ("Guardrails", "*guard")]),
    ("ML & Retrieval", [("PyTorch", "pytorch.svg"), ("Scikit-learn", "scikitlearn.svg"), ("XGBoost", "xgboost.webp"), ("pgvector", "*vector"),
                        ("Hybrid Retrieval", "*hybrid"), ("MLflow", "mlflow.svg")]),
    ("Backend", [("FastAPI", "fastapi.svg"), ("WebSockets", "websocket.svg"), ("Next.js", "nextjs.svg"), ("E2B Sandboxes", "e2b.webp")]),
    ("Cloud & Data", [("PostgreSQL", "postgresql.svg"), ("Supabase", "supabase.svg"), ("SQLite", "sqlite.svg"), ("Docker", "docker.svg"),
                      ("AWS", "aws.svg"), ("GitHub Actions", "githubactions.svg")]),
]
WIDE = {"aws.svg": 1.12, "scikitlearn.svg": 1.2, "xgboost.webp": 1.28, "langchain.svg": 1.22, "langgraph.svg": 1.22, "docker.svg": 1.15, "e2b.webp": .92}

_L = 'fill="none" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"'
DRAWN = {  # 24 x 24
    "sql": f'<path d="M4 5.5V18.5C4 20.4 7.6 22 12 22s8-1.6 8-3.5V5.5" fill="#E8F0FE" stroke="#1A73E8" stroke-width="1.8"/><path d="M4 12c0 1.9 3.6 3.5 8 3.5s8-1.6 8-3.5" {_L} stroke="#1A73E8"/>'
           '<ellipse cx="12" cy="5.5" rx="8" ry="3.5" fill="#1A73E8"/>',
    "agents": f'<path d="M12 12L12 4.5M12 12L5 18M12 12L19 18" {_L} stroke="#A78BFA"/><circle cx="12" cy="4.2" r="3" fill="#7C3AED"/><circle cx="4.8" cy="18.6" r="3" fill="#2563EB"/>'
              '<circle cx="19.2" cy="18.6" r="3" fill="#EC4899"/><circle cx="12" cy="12" r="3.6" fill="#111827"/>',
    "rag": f'<path d="M4 3h9l4 4v5" {_L} stroke="#059669"/><path d="M4 3v18h6.5" {_L} stroke="#059669"/><path d="M7.5 9h5M7.5 13h3" {_L} stroke="#6EE7B7"/>'
           f'<circle cx="15.5" cy="16" r="4" fill="#D1FAE5" stroke="#059669" stroke-width="2.1"/><path d="M18.5 19L21.5 22" {_L} stroke="#059669"/>',
    "tool": '<path d="M20.8 6.2l-3.4 3.4-3-.6-.6-3 3.4-3.4a6 6 0 0 0-7.7 7.8L3 17a2.8 2.8 0 0 0 4 4l6.6-6.5a6 6 0 0 0 7.2-8.3z" fill="#F97316"/><circle cx="5.2" cy="18.8" r="1.2" fill="#FFF"/>',
    "route": f'<path d="M3 12h5c4 0 3.500-7 8-7h4M8 12h12M8 12c4 0 3.500 7 8 7h4" {_L} stroke="#0891B2"/><circle cx="4" cy="12" r="2.6" fill="#0E7490"/>'
             '<circle cx="20" cy="5" r="2.4" fill="#22D3EE"/><circle cx="20" cy="12" r="2.4" fill="#06B6D4"/><circle cx="20" cy="19" r="2.4" fill="#F59E0B"/>',
    "guard": f'<path d="M12 2l8 3v6.500c0 5-3.400 8.700-8 10.500-4.600-1.800-8-5.500-8-10.500V5z" fill="#16A34A"/><path d="M12 2l8 3v6.500c0 5-3.400 8.700-8 10.500z" fill="#15803D"/><path d="M8 12l2.800 2.800L16 9.400" {_L} stroke="#FFF"/>',
    "vector": f'<path d="M4 20V4M4 20h16" {_L} stroke="#94A3B8"/><path d="M4 20L18.500 6.500M13.500 6h5.200v5.200" {_L} stroke="#336791"/><path d="M4 20L11 6" {_L} stroke="#5B9BD5"/><circle cx="11" cy="5.600" r="2.200" fill="#5B9BD5"/><circle cx="19" cy="15" r="2.200" fill="#336791"/>',
    "hybrid": f'<circle cx="8.500" cy="9" r="6" fill="#6366F1" fill-opacity=".85"/><circle cx="14" cy="9" r="6" fill="#F43F5E" fill-opacity=".75"/><path d="M16.500 16L21.500 21.500" {_L} stroke="#111827"/><path d="M11.250 4.100a6 6 0 0 1 0 9.800 6 6 0 0 1 0-9.800z" fill="#FDE047"/>',
}


def logo(name, cx, cy, size):
    """Each logo is embedded as its own image, so ids and styles inside it cannot clash."""
    if name.startswith("*"):
        k = size * .94 / 24
        return f'<g transform="translate({cx - 12 * k:.2f} {cy - 12 * k:.2f}) scale({k:.3f})">{DRAWN[name[1:]]}</g>'
    size *= WIDE.get(name, 1)
    mime = "image/svg+xml" if name.endswith("svg") else "image/webp"
    data = base64.b64encode((ICONS / name).read_bytes()).decode()
    return f'<image x="{cx - size / 2:.2f}" y="{cy - size / 2:.2f}" width="{size:.2f}" height="{size:.2f}" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{data}"/>'


def cell(cx, y, tile, label, name, size, order):
    """A white app tile with the logo, and its name below on one or two lines."""
    words = label.split(" ")
    lines = [label] if len(words) == 1 else [words[0], " ".join(words[1:])]
    out = (f'<g class="tile" style="animation-delay:{order * .11:.2f}s"><rect x="{cx - tile / 2:.1f}" y="{y}" width="{tile}" height="{tile}" rx="{tile * .27:.1f}" fill="#FFF"/>'
           + logo(name, cx, y + tile / 2, tile * .62) + "</g>")
    return out + "".join(text(cx, y + tile + 20 + i * 16.5, s, size, V["text"], weight=500, anchor="middle") for i, s in enumerate(lines))


CSS = ("@keyframes ti{0%,14%,100%{transform:none}5%{transform:translateY(-7px) scale(1.06)}10%{transform:translateY(1px)}}"
       ".tile{transform-box:fill-box;transform-origin:center;animation:ti 7s ease-in-out infinite}")


def skills(m=False):
    b, n = [], 0
    if m:
        w, y, step, tile = MW, 6, (MW - 2 * MP + 8) / 4, 56
        for i, (group, items) in enumerate(SKILLS):
            if i:
                b.append(hline(MP, y, w - MP))
            b.append(text(MP, y + 38, group, 17, V["text"], weight=600))
            for j, (label, name) in enumerate(items):
                b.append(cell(MP - 4 + (j % 4 + .5) * step, y + 60 + (j // 4) * 112, tile, label, name, 13.5, n))
                n += 1
            y += 60 + ((len(items) - 1) // 4 + 1) * 112
        h = round(y + 6)
    else:
        w, rh, top, step, tile = W, 130, 8, 94, 58
        h = top * 2 + rh * len(SKILLS)
        for i, (group, items) in enumerate(SKILLS):
            y = top + i * rh
            if i:
                b.append(hline(P, y, w - P))
            b.append(text(P, y + 57, group, 18, V["text"], weight=600))
            for j, (label, name) in enumerate(items):
                b.append(cell(200 + (j + .5) * step - 3, y + 20, tile, label, name, 13.5, n))
                n += 1
    desc = "; ".join(f"{g}: {', '.join(s for s, _ in items)}" for g, items in SKILLS)
    return doc(w, h, "Technical skills", desc, surface(w, h) + "".join(b), CSS)
