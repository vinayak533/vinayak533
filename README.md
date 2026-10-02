<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/hero-dark-compact.svg">
  <img src="assets/svg/hero-dark.svg" width="100%" alt="VINAYAK — AI/ML Engineer at AMnova Technologies, Kochi, India. AI systems that show their work: agents that run real tools, answers that cite or abstain. HackerRank Orchestrate finalist. A butterfly drawn in white and violet dots flies across the banner behind the text, trailing violet stardust.">
</picture>

<p>
  <a href="https://www.linkedin.com/in/vinayak-kv-ds"><img src="assets/svg/link-linkedin-dark.svg" height="34" alt="LinkedIn"></a>&nbsp;
  <a href="https://vinayak533.github.io/VINAYAK_PORTFOLIO/"><img src="assets/svg/link-portfolio-dark.svg" height="34" alt="Portfolio"></a>&nbsp;
  <a href="mailto:vinayakkvjob@gmail.com"><img src="assets/svg/link-email-dark.svg" height="34" alt="Email"></a>
</p>

I build agent systems, grounded LLM applications and ML pipelines that expose how they work: live tool traces, cited sources, tested guardrails and documented limits. AI/ML Engineer at **AMnova Technologies**, Kochi.

<br>

### Expertise

<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/expertise-dark-compact.svg">
  <img src="assets/svg/expertise-dark.svg" width="100%" alt="Agent systems (loom.ai): tool execution in a real Linux sandbox, model routing with provider fallback. Grounded generation (loom.ai, lazyhire): answers that cite sources or abstain; CV drafts checked for invented claims. Applied ML (InForge-AI, InsightGenie, NL2SQL): cleaning, EDA and model benchmarking, with local fallbacks when LLMs fail. Product engineering (loom.ai, lazyhire, InForge-AI): WebSocket backends and Next.js products, hardened with CSP, CSRF and E2E tests.">
</picture>

<br>

### Selected work

<a href="https://github.com/vinayak533/loom.ai">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-loom-dark-compact.svg">
  <img src="assets/svg/card-loom-dark.svg" width="100%" alt="loom.ai, flagship agent workspace: a coding agent inside a real Linux sandbox that streams every tool call. Request path: Next.js trace UI, FastAPI WebSocket, LangGraph, model router with fallback, tools, E2B sandbox. Median time-to-first-token 8.9s to 5.0s; 8 models across Groq, OpenRouter and OpenCode; 10 specialist agents with human approval. Open repository.">
</picture>
</a>

<a href="https://github.com/vinayak533/loom.ai#-project-showcase">
<img src="assets/svg/screen-loom-dark.svg" width="100%" alt="loom.ai's Code workspace: timed tool calls in the agent trace beside the file the agent wrote. Real interface; scripted demo turn.">
</a>

<sub>Real interface. The agent turn is scripted and played through the live WebSocket UI — <a href="https://github.com/vinayak533/loom.ai#-project-showcase">capture notes</a>.</sub>

[Repository ↗](https://github.com/vinayak533/loom.ai) &nbsp;·&nbsp; [Architecture](https://github.com/vinayak533/loom.ai/blob/main/docs/architecture.md) &nbsp;·&nbsp; [Known limits](https://github.com/vinayak533/loom.ai/blob/main/docs/known-limits.md)

<details>
<summary>Engineering notes &amp; more screens</summary>

- **Execution** — one typed WebSocket event contract connects the LangGraph agent to the interface. Read-only tool batches run concurrently; writes run in order. Graph checkpoints let sessions survive a cold start.
- **Routing** — each iteration is classified and sent to the model registered for that class. Rate limits, quota and 5xx errors retry on up to two alternate providers. Message and usage writes stay off the token path.
- **Measured** — median time-to-first-token fell from 8.9s to 5.0s on a ~80K-token loop once the transcript was served from the provider's prompt cache. [Method](https://github.com/vinayak533/loom.ai/blob/main/docs/performance.md).
- **Grounding** — notebooks answer only from uploaded sources with `[n]` citations, or say the sources don't cover it. Retrieval uses lexical hashed vectors, not semantic search.
- **Scope** — Chat, Code, Learn (ten authored courses) and ten specialist agents with human approval. Code needs an E2B key; AI features need a model-provider key.

<img src="assets/screens/loom-specialists.png" width="100%" loading="lazy" alt="Gallery of ten specialist agents, each listing its role and the tools it can call.">

<img src="assets/screens/loom-learn.png" width="100%" loading="lazy" alt="Learn course catalogue with progress, assessments and a resume banner.">

</details>

<br>

<a href="https://github.com/vinayak533/lazyhire">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-lazyhire-dark-compact.svg">
  <img src="assets/svg/card-lazyhire-dark.svg" width="100%" alt="lazyhire: a private career workspace that ranks Kerala job listings against your CV. Pipeline: 9 sources, validate apply links, dedupe, rank and explain, guarded CV drafts. Next.js 16, React 19, TypeScript, SQLite with Drizzle, Playwright. Zero-fabrication CV guardrails. Open repository.">
</picture>
</a>

<details>
<summary>Engineering notes &amp; product screens</summary>

- **Discovery** — nine Kerala sources (Technopark, Infopark, UL CyberPark and others) feed apply-link validation, then deduplication on canonical URL plus company, title and location, then ranking by freshness, source quality, location, role fit and skills.
- **AI boundary** — the assistant answers from an authored knowledge corpus before any optional LLM call. Tailored CVs are rejected if they add numbers, requirements or changes that can't be traced to the source CV.
- **Privacy** — encrypted CV and account data, per-request CSP nonces, CSRF checks on every mutation, private-response cache controls, upload scanning and audit events. SQLite with Drizzle migrations keeps setup self-contained.
- **Verification** — Node tests and Playwright cover auth, discovery, CV workflows, Career OS and privacy boundaries.

<img src="assets/screens/lazyhire-career-os.png" width="100%" loading="lazy" alt="Career OS: readiness, gaps and roadmap derived from CV evidence and saved applications. Seeded example data.">

<sub>Career OS, seeded example data.</sub>

<img src="assets/screens/lazyhire-matches.png" width="100%" loading="lazy" alt="Ranked job matches with source counts, explained fit and duplicate detection. Fixture listings.">

<sub>Ranked matches, fixture listings.</sub>

<img src="assets/screens/lazyhire-cv-review.png" width="100%" loading="lazy" alt="CV review with a server-side writing score and an optional AI fit review.">

</details>

<br>

<a href="https://github.com/vinayak533/InForge-AI">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-inforge-dark-compact.svg">
  <img src="assets/svg/card-inforge-dark.svg" width="100%" alt="InForge-AI: eight pipeline agents turn a CSV or Excel file into analysis, models and a report. Pipeline: ingest, clean, EDA, visualize, ML benchmark, insights, code, chat. FastAPI, WebSockets, pandas, scikit-learn, XGBoost, React. Completes without an LLM provider. Open repository.">
</picture>
</a>

<details>
<summary>Engineering notes</summary>

- **Pipeline** — an orchestrator runs eight agents in order and streams each stage over a WebSocket; late-connecting clients are replayed the history.
- **Deterministic core** — pandas, scikit-learn and XGBoost compute every result. LLMs (OpenRouter, Groq, Gemini) only write explanations, chart strategy, code and chat answers.
- **Resilience** — every LLM call has a local fallback, so an invalid key, rate limit or outage degrades the prose, not the analysis.
- **Outputs** — cleaned CSV, charts, benchmarked models, a PDF report, Python code and contextual chat. Runs locally.

</details>

<details>
<summary>More projects — retrieval, evaluation &amp; applied ML</summary>

- [**NL2SQL-AI-Assistant**](https://github.com/vinayak533/NL2SQL-AI-Assistant) — validated SQL over a clinic database; 18/20 on its own benchmark. Vanna 2.0 · Gemini · FastAPI
- [**llm-battle-arena**](https://github.com/vinayak533/llm-battle-arena) — two models answer, a third judges with structured verdicts. LlamaIndex · Groq
- [**InsightGenie**](https://github.com/vinayak533/InsightGenie-Data-Analyzer) — CSV health checks, charts and rule-based ML recommendations. FastAPI · React · pandas
- [**ARIA churn platform**](https://github.com/vinayak533/bank-churn-intelligence-platform) — XGBoost churn estimates, explained by an LLM and read aloud. FastAPI · Groq · ElevenLabs
- [**PredictLab**](https://github.com/vinayak533/PredictLab-) — three health-risk classifiers behind one API. scikit-learn · FastAPI · Docker
- [**Medical Voice & Vision**](https://github.com/vinayak533/AI-Medical-Voice-Vision-Assistant) — spoken question plus image in, spoken answer out. Groq · Gradio · gTTS
- [**Multi-agent stock analysis**](https://github.com/vinayak533/AI-Multi-Agent-Stock-Analysis-Trading-System) — two agents turn a price snapshot into a Buy/Sell/Hold rationale. CrewAI · yfinance · Streamlit

</details>

<br>

### GitHub activity

<a href="https://github.com/vinayak533?tab=overview">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/activity-dark-compact.svg">
  <img src="assets/svg/activity-dark.svg" width="100%" alt="Weekly GitHub contributions over the last year as a dot matrix, with the last 90 days highlighted. Refreshed daily from GitHub’s contribution calendar by a repository workflow.">
</picture>
</a>

<br>

### Tech stack

<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/stack-dark-compact.svg">
  <img src="assets/svg/stack-dark.svg" width="100%" alt="AI / ML: pandas, NumPy, scikit-learn, XGBoost. LLMs and agents: LangGraph, CrewAI, LlamaIndex, Vanna 2.0, OpenAI SDK. Model APIs: Groq, Gemini, OpenRouter. Backend: Python, FastAPI, WebSockets, Pydantic. Frontend: TypeScript, Next.js, React, Tailwind CSS. Data: PostgreSQL, Supabase, pgvector, SQLite, Drizzle. Cloud and delivery: E2B, Docker, GitHub Actions, Playwright, Vercel, Render.">
</picture>

<sub>Only technologies declared in the dependency files of the projects above.</sub>

<br>

### Contact

<a href="mailto:vinayakkvjob@gmail.com">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/contact-dark-compact.svg">
  <img src="assets/svg/contact-dark.svg" width="100%" alt="Let’s build AI that shows its work. Open to AI/ML and LLM engineering roles: remote, Bangalore, Kochi or Hyderabad. Email vinayakkvjob@gmail.com.">
</picture>
</a>

[LinkedIn](https://www.linkedin.com/in/vinayak-kv-ds) &nbsp;·&nbsp; [Portfolio](https://vinayak533.github.io/VINAYAK_PORTFOLIO/) &nbsp;·&nbsp; [All repositories](https://github.com/vinayak533?tab=repositories)
