<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/hero-dark.svg">
  <img src="assets/svg/hero-light.svg" width="100%" alt="Vinayak K V. AI/ML Engineer: agent systems, LLM infrastructure, applied ML. I build agent systems that run real tools, route across models, and refuse to make things up.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/status-dark.svg">
  <img src="assets/svg/status-light.svg" width="100%" alt="Role: AI/ML Engineer at AMnova. Base: Kochi, India. Focus: agent systems and LLM infrastructure. Now building: loom.ai.">
</picture>

</div>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-01-dark.svg">
  <img src="assets/svg/sec-01-light.svg" width="100%" alt="01 Console">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/terminal-dark.svg">
  <img src="assets/svg/terminal-light.svg" width="100%" alt="whoami: Vinayak K V, AI/ML Engineer, Kochi. Systems: loom.ai, lazyhire, inforge-ai, nl2sql, llm-battle-arena. Focus: agent graphs that run real tools; one interface over many models, with fallback; retrieval that cites its sources or abstains; generated text checked for fabrication.">
</picture>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-02-dark.svg">
  <img src="assets/svg/sec-02-light.svg" width="100%" alt="02 System map">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/system-map-dark.svg">
  <img src="assets/svg/system-map-light.svg" width="100%" alt="Engineering system map. Agents and LLMs: agent graphs with real tools, model router with fallback, retrieval with citations, LLM-as-judge evaluation. Product systems: streaming WebSocket backends, Next.js and TypeScript products, auth/CSP/CSRF/encryption, E2E tests and CI. Data and ML: multi-agent analytics pipeline, model benchmarking, natural language to SQL, dataset health profiling. Each capability names the repository that implements it.">
</picture>

<sub>Every capability names the repository that implements it.</sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-03-dark.svg">
  <img src="assets/svg/sec-03-light.svg" width="100%" alt="03 Selected systems">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/card-loom-dark.svg">
  <img src="assets/svg/card-loom-light.svg" width="100%" alt="loom.ai: an AI workspace where a coding agent works inside a real Linux sandbox. Problem: chat agents can't run the code they write or show their work. System: WebSocket event stream, LangGraph, tools, E2B sandbox. Intelligence: 8 models across 3 providers, task-classified routing, fallback on rate limits and 5xx. Result: live trace and preview, 10 specialist agents, median time-to-first-token 8.9s to 5.0s.">
</picture>

<sub><a href="https://github.com/vinayak533/loom.ai"><b>github.com/vinayak533/loom.ai</b></a></sub>

<img src="assets/screens/loom-agent-trace.png" width="100%" alt="loom.ai Code workspace: the agent's step-by-step trace with timed tool calls on the left, and the file it wrote open in the inline editor on the right.">

<sub>Code workspace: each tool call is a timed card in the trace, and the files it writes open in the editor. This is a scripted demo turn played through the real UI; the repo's README explains how it was captured.</sub>

<details>
<summary><b>More from loom.ai</b>: specialist agents, Learn</summary>
<br>
<img src="assets/screens/loom-specialists.png" width="100%" alt="Gallery of ten specialist agents, each card listing its role and the tools it can call.">
<sub>Ten specialists, each a separate agent with its own persona and toolset.</sub>
<br><br>
<img src="assets/screens/loom-learn.png" width="100%" alt="Course catalogue with progress, assessments, and a resume banner.">
<sub>Learn: ten authored courses with server-graded assessments and weak-area review.</sub>
</details>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/card-lazyhire-dark.svg">
  <img src="assets/svg/card-lazyhire-light.svg" width="100%" alt="lazyhire: a private career workspace that ranks Kerala job openings against your CV. Problem: duplicate listings, dead apply links, inflated CV rewrites. System: 9 sources, validation, dedupe, ranking; Next.js 16 and SQLite. Intelligence: CV review and tailoring with a no-fabrication guard, knowledge-first tutor. Result: explained fit scores, AES-GCM encrypted CV storage, Playwright E2E suite.">
</picture>

<sub><a href="https://github.com/vinayak533/lazyhire"><b>github.com/vinayak533/lazyhire</b></a></sub>

<img src="assets/screens/lazyhire-career-os.png" width="100%" alt="lazyhire Career OS: profile evidence, priority gaps, readiness score, roadmap and data-confidence panel.">

<sub>Career OS: readiness, gaps and a roadmap computed only from CV evidence and saved applications. Seeded example data.</sub>

<details>
<summary><b>More from lazyhire</b>: ranked matches, CV review</summary>
<br>
<img src="assets/screens/lazyhire-matches.png" width="100%" alt="Ranked job matches with per-source counts, fit scores, matched skills and duplicate-source badges.">
<sub>Ranked matches with per-source counts, the skills behind each fit score, and cross-source duplicate detection. Fixture listings.</sub>
<br><br>
<img src="assets/screens/lazyhire-cv-review.png" width="100%" alt="CV review with a rule-based writing score and an optional AI fit review.">
<sub>CV review: a rule-based writing score that runs on the server, plus an optional AI review that only runs when you ask for it.</sub>
</details>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/card-inforge-dark.svg">
  <img src="assets/svg/card-inforge-light.svg" width="100%" alt="InForge-AI: eight pipeline agents turn a raw CSV or Excel file into analysis, models and a report. Problem: hours of profiling and cleaning before the first insight. System: 8 agents in sequence, WebSocket progress, FastAPI and React. Intelligence: scikit-learn and XGBoost compute, LLMs write the prose, heuristics if an LLM call fails. Result: cleaned data and charts, benchmarked models, PDF report and code.">
</picture>

<sub><a href="https://github.com/vinayak533/InForge-AI"><b>github.com/vinayak533/InForge-AI</b></a></sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-04-dark.svg">
  <img src="assets/svg/sec-04-light.svg" width="100%" alt="04 Architecture">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/arch-loom-dark.svg">
  <img src="assets/svg/arch-loom-light.svg" width="100%" alt="loom.ai request path: the browser sends user_message over a WebSocket to FastAPI; LangGraph asks the model router, which picks a model by task class and falls back across OpenCode, OpenRouter and Groq; tool_use routes to tool nodes that execute in an E2B sandbox; events stream back to the browser; writes to Supabase are fire-and-forget; the sandbox dev server is forwarded to a live preview.">
</picture>

<sub><b>loom.ai, one Code turn.</b> Blue is the request; amber is what streams back. The router shows a rate-limited provider falling over to the next one.</sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/arch-lazyhire-dark.svg">
  <img src="assets/svg/arch-lazyhire-light.svg" width="100%" alt="lazyhire. Discovery: career brief, 9 job sources, apply-link validation, merge and dedupe, rank and explain. AI path: question or CV task, privacy and CSRF checks, authored knowledge first, optional LLM (DeepSeek then Groq), guarded output that rejects invented numbers.">
</picture>

<sub><b>lazyhire.</b> Discovery is deterministic. The model is optional and sits behind privacy checks and a fabrication guard.</sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/arch-inforge-dark.svg">
  <img src="assets/svg/arch-inforge-light.svg" width="100%" alt="InForge-AI: eight stages run in order (ingest, clean, EDA, visualize, ML, insights, code, chat). A deterministic core computes results; optional LLM enrichment writes prose, with local heuristics when a call fails.">
</picture>

<sub><b>InForge-AI.</b> Every number comes from the deterministic core; the LLMs only write the explanations.</sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-05-dark.svg">
  <img src="assets/svg/sec-05-light.svg" width="100%" alt="05 Engineering notes">
</picture>

<details open>
<summary><b>loom.ai</b>: agent workspace · Python + TypeScript</summary>

<br>

| | |
|---|---|
| **Challenge** | A coding agent is only useful if it can run what it writes, and if you can watch it do so. |
| **Engineering** | One typed event contract (`events.py` ⇄ `events.ts`) is the only interface between the agent and the UI. Tokens, tool calls, stdout chunks, file diffs and preview readiness all travel over one WebSocket. |
| **Intelligence** | A LangGraph `StateGraph` streams each model call; conditional edges route every `tool_use` to its node. A classifier labels each iteration (`fast_simple`, `code_editing`, `visual_structural`, `complex_longhorizon`) and routes it to the model registered for that class, across Groq, OpenRouter and OpenCode. |
| **System design** | Read-only tool batches run concurrently; writes run in order. Message and usage writes are fire-and-forget, so nothing sits on the token path. Graph state is checkpointed (SQLite locally, Postgres in production), so sessions survive a cold start. |
| **Measured** | On a ~80K-token loop, median time-to-first-token went from **8.9s to 5.0s** once the transcript was served from the provider's prompt cache ([`docs/performance.md`](https://github.com/vinayak533/loom.ai/blob/main/docs/performance.md)). |
| **Works today** | Chat, Code (E2B sandbox, live preview, terminal, git), Learn (10 courses, notebooks that cite their sources) and 10 specialist agents with human approval. A stated limit: notebook retrieval is lexical (hashed bag-of-words), not semantic. |

</details>

<details>
<summary><b>lazyhire</b>: career workspace · TypeScript</summary>

<br>

| | |
|---|---|
| **Challenge** | The same job appears on several portals, apply links often lead to homepages, and AI CV rewriters invent experience. |
| **Engineering** | One adapter per source (Technopark, Infopark, UL CyberPark, Indeed and others) feeds apply-link validation. Listings are merged on canonical URL plus company, normalized title and location, then ranked on freshness, source quality, location, role fit and skill overlap. |
| **Intelligence** | CV review and tailoring go through a DeepSeek-compatible model with Groq as fallback. `tailor-guardrails.ts` rejects drafts with numbers (including spelled-out ones), requirements or changes that can't be traced to the source CV. The assistant answers from an authored knowledge corpus before it calls an LLM. |
| **System design** | Per-request CSP nonce, CSRF protection on every mutation, AES-256-GCM for CV and account data, `no-store` on private responses, upload scanning and audit events. SQLite with Drizzle migrations, so it runs without managed infrastructure. |
| **Works today** | Discovery, ranked matches, an application pipeline, CV parse/review/tailor, Career OS and the assistant. Node tests and Playwright E2E cover auth, discovery, links, CV, Career OS and privacy boundaries. |

</details>

<details>
<summary><b>InForge-AI</b>: analytics pipeline · Python + React</summary>

<br>

| | |
|---|---|
| **Challenge** | The first hours with any new dataset go into profiling and cleaning before any analysis starts. |
| **Engineering** | An orchestrator runs eight agents in order and streams each stage's state over a WebSocket. Clients that connect late are replayed the history. |
| **Intelligence** | pandas, scikit-learn and XGBoost do the analysis: problem-type detection, cleaning, EDA and model comparison. LLMs (OpenRouter, Groq, Gemini) write the explanations, chart strategy, generated code and chat answers. |
| **System design** | Every LLM call has a local fallback. An invalid key, rate limit or outage degrades the prose, not the results. |
| **Works today** | CSV/XLS/XLSX in → cleaned data, charts, benchmarked models, a PDF report, Python code and contextual chat. Runs locally; the hosted demo's backend is currently offline. |

</details>

<br>

**Also built**

| Project | What it does | Stack |
|---|---|---|
| [NL2SQL-AI-Assistant](https://github.com/vinayak533/NL2SQL-AI-Assistant) | Plain-English questions → validated SQL over a clinic database. 18 of 20 on its own benchmark. | Vanna 2.0 · Gemini · FastAPI |
| [llm-battle-arena](https://github.com/vinayak533/llm-battle-arena) | Two models answer, a third judges (LLM-as-a-judge, JSON verdicts) | LlamaIndex · Groq |
| [InsightGenie](https://github.com/vinayak533/InsightGenie-Data-Analyzer) | CSV health checks, charts and rule-based ML recommendations | FastAPI · React · pandas |
| [ARIA churn platform](https://github.com/vinayak533/bank-churn-intelligence-platform) | XGBoost churn estimate, explained by an LLM and read aloud | FastAPI · XGBoost · Groq · ElevenLabs |
| [PredictLab](https://github.com/vinayak533/PredictLab-) | Three health-risk classifiers behind one FastAPI app | scikit-learn · FastAPI · Docker |
| [Medical Voice & Vision](https://github.com/vinayak533/AI-Medical-Voice-Vision-Assistant) | Spoken question + image → transcribed, answered, spoken back | Groq · Gradio · gTTS |
| [Multi-agent stock analysis](https://github.com/vinayak533/AI-Multi-Agent-Stock-Analysis-Trading-System) | Two CrewAI agents turn a price snapshot into a Buy/Sell/Hold rationale | CrewAI · yfinance · Streamlit |

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-06-dark.svg">
  <img src="assets/svg/sec-06-light.svg" width="100%" alt="06 Stack">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/stack-dark.svg">
  <img src="assets/svg/stack-light.svg" width="100%" alt="Engineering stack. Agents: LangGraph, CrewAI, LlamaIndex, Vanna 2.0. Models: Groq, Gemini, OpenRouter, OpenAI SDK, tiktoken. Backend: Python, FastAPI, WebSockets, Pydantic. Applied ML: pandas, NumPy, scikit-learn, XGBoost. Data: Supabase Postgres, pgvector, SQLite, Drizzle ORM. Frontend: TypeScript, Next.js, React, Tailwind, Framer Motion. Delivery: E2B, Docker, GitHub Actions, Playwright, Vercel, Render.">
</picture>

<sub>Only technologies declared in the dependency files of the projects above.</sub>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-07-dark.svg">
  <img src="assets/svg/sec-07-light.svg" width="100%" alt="07 Activity">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/activity-dark.svg">
  <img src="assets/svg/activity-light.svg" width="100%" alt="Contribution calendar for the last 12 months, regenerated daily from GitHub data.">
</picture>

<br><br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-08-dark.svg">
  <img src="assets/svg/sec-08-light.svg" width="100%" alt="08 Principles">
</picture>

**`DETERMINISTIC CORE`**
Compute what can be computed. InForge-AI cleans, profiles and benchmarks with pandas and scikit-learn, and still finishes when every LLM call fails.

**`CITE OR ABSTAIN`**
loom.ai's notebooks answer only from uploaded sources with `[n]` citations, or say the sources don't cover the question. lazyhire rejects tailored CVs that introduce numbers the original doesn't contain.

**`FAIL OVER, NOT OUT`**
A rate-limited provider should trigger a reroute, not an error page. loom.ai retries on up to two alternate providers and bills only for the model that answered.

**`WRITE DOWN THE LIMITS`**
Each flagship README has a limits section: lexical retrieval, single-instance rate limits, and which screenshots are scripted.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-09-dark.svg">
  <img src="assets/svg/sec-09-light.svg" width="100%" alt="09 Credentials">
</picture>

| Credential | Context |
|---|---|
| **AI/ML Engineer** | AMnova Technologies · Kochi |
| **Top 2% globally** | LeetCode |
| **Finalist** | HackerRank Orchestrate Hackathon |

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/sec-10-dark.svg">
  <img src="assets/svg/sec-10-light.svg" width="100%" alt="10 Contact">
</picture>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/svg/footer-dark.svg">
  <img src="assets/svg/footer-light.svg" width="100%" alt="Systems that show their work: traces, citations, tests, documented limits.">
</picture>

Open to AI/ML and LLM engineering roles: remote, Bangalore, Kochi or Hyderabad.

[LinkedIn](https://www.linkedin.com/in/vinayak-kv-ds) &nbsp;·&nbsp; [Portfolio](https://vinayak533.github.io/VINAYAK_PORTFOLIO/) &nbsp;·&nbsp; [vinayakkvjob@gmail.com](mailto:vinayakkvjob@gmail.com)

</div>
