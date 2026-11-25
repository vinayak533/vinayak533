<p>
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/hero-compact.svg">
  <img src="assets/svg/hero.svg" width="100%" alt="VINAYAK — AI/ML Engineer, Kochi, India. AI systems that show their work: agents that run real tools, answers that cite or abstain. HackerRank Orchestrate finalist. A butterfly drawn in white and violet dots flies across the banner behind the text, trailing violet stardust.">
</picture>
</p>

<p>
  <a href="https://www.vinayakkv.com/Vinayak_CV.pdf"><img src="assets/svg/link-resume.svg" height="34" alt="Resume (PDF)"></a>
  <a href="https://www.vinayakkv.com/"><img src="assets/svg/link-portfolio.svg" height="34" alt="Portfolio"></a>
  <a href="https://www.linkedin.com/in/vinayak-kv-ds"><img src="assets/svg/link-linkedin.svg" height="34" alt="LinkedIn"></a>
  <a href="mailto:vinayakkvjob@gmail.com"><img src="assets/svg/link-email.svg" height="34" alt="Email"></a>
</p>

I build agent systems, grounded LLM applications and ML pipelines that expose how they work: live tool traces, cited sources, tested guardrails and documented limits. AI/ML Engineer at **AMnova Technologies**, Kochi.

**Open to AI/ML roles.**

<p>
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/proof-compact.svg">
  <img src="assets/svg/proof.svg" width="100%" alt="44% less time to first token in loom.ai, from 8.9s to 5.0s. 10 specialist agents with human approval. 18 of 20 correct SQL answers on NL2SQL&#39;s own benchmark. 1 published paper with a Zenodo DOI, sole author.">
</picture>
</p>

### Selected work

<a href="https://github.com/vinayak533/loom.ai">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-loom-compact.svg">
  <img src="assets/svg/card-loom.svg" width="100%" alt="loom.ai, flagship agent workspace: a coding agent inside a real Linux sandbox that streams every tool call. Animated replay of the repository's scripted demo turn: a prompt is sent, terminal, write and dev-server calls complete, and App.tsx is written. Request path: Next.js, FastAPI WebSocket, LangGraph, model router with fallback, tools, E2B sandbox. A race drawn in real seconds compares median time-to-first-token before, 8.9s, and after prompt caching, 5.0s. 8 models across Groq, OpenRouter and OpenCode; 10 specialist agents with human approval. Open repository.">
</picture>
</a>

<sub>Animated replay of the repository's scripted demo turn. Real screens are in the notes below: <a href="https://github.com/vinayak533/loom.ai#-project-showcase">capture notes</a>.</sub>

[Repository ↗](https://github.com/vinayak533/loom.ai) &nbsp;·&nbsp; [Architecture](https://github.com/vinayak533/loom.ai/blob/main/docs/architecture.md) &nbsp;·&nbsp; [Known limits](https://github.com/vinayak533/loom.ai/blob/main/docs/known-limits.md)

<details>
<summary>Engineering notes &amp; more screens</summary>

- **Execution** — one typed WebSocket event contract connects the LangGraph agent to the interface. Read-only tool batches run concurrently; writes run in order. Graph checkpoints let sessions survive a cold start.
- **Routing** — each iteration is classified and sent to the model registered for that class. Rate limits, quota and 5xx errors retry on up to two alternate providers. Message and usage writes stay off the token path.
- **Measured** — median time-to-first-token fell from 8.9s to 5.0s on a ~80K-token loop once the transcript was served from the provider's prompt cache. [Method](https://github.com/vinayak533/loom.ai/blob/main/docs/performance.md).
- **Grounding** — notebooks answer only from uploaded sources with `[n]` citations, or say the sources don't cover it. Retrieval uses lexical hashed vectors, not semantic search.
- **Scope** — Chat, Code, Learn (ten authored courses) and ten specialist agents with human approval. Code needs an E2B key; AI features need a model-provider key.

<img src="assets/screens/loom-agent-trace.png" width="100%" loading="lazy" alt="loom.ai's Code workspace: timed tool calls in the agent trace beside the file the agent wrote. Real interface, scripted demo turn.">

<img src="assets/screens/loom-specialists.png" width="100%" loading="lazy" alt="Gallery of ten specialist agents, each listing its role and the tools it can call.">

<img src="assets/screens/loom-learn.png" width="100%" loading="lazy" alt="Learn course catalogue with progress, assessments and a resume banner.">

</details>

<br>

<a href="https://github.com/vinayak533/lazyhire">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-lazyhire-compact.svg">
  <img src="assets/svg/card-lazyhire.svg" width="100%" alt="lazyhire: a private career workspace that ranks Kerala job listings against your CV. Animated illustration with fixture listings: postings from several of its nine sources move through apply-link validation, deduplication and ranking; dead links and duplicates drop out, and survivors are ranked with the reason they match. A CV draft line that cannot be traced to the source CV is struck out and rejected. Next.js 16, React 19, TypeScript, SQLite with Drizzle, Playwright. Zero-fabrication CV guardrails. Open repository.">
</picture>
</a>

<sub>Animated illustration with fixture listings. Real screens are in the notes below.</sub>

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
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-inforge-compact.svg">
  <img src="assets/svg/card-inforge.svg" width="100%" alt="InForge-AI: eight pipeline agents turn a CSV or Excel file into analysis, models and a report. Animated illustration: ingest, clean, EDA, visualize, ML benchmark, insights, code and chat run in order; missing cells are repaired, a trend is drawn, candidate models are compared. At insights the LLM provider fails, a local fallback takes over, and the run still completes. FastAPI, WebSockets, pandas, scikit-learn, XGBoost, React. Completes without an LLM provider. Open repository.">
</picture>
</a>

<sub>Animated illustration of one run, including a provider failure.</sub>

<details>
<summary>Engineering notes</summary>

- **Pipeline** — an orchestrator runs eight agents in order and streams each stage over a WebSocket; late-connecting clients are replayed the history.
- **Deterministic core** — pandas, scikit-learn and XGBoost compute every result. LLMs (OpenRouter, Groq, Gemini) only write explanations, chart strategy, code and chat answers.
- **Resilience** — every LLM call has a local fallback, so an invalid key, rate limit or outage degrades the prose, not the analysis.
- **Outputs** — cleaned CSV, charts, benchmarked models, a PDF report, Python code and contextual chat. Runs locally.

</details>

### Research

<a href="https://doi.org/10.5281/zenodo.20253956">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-paper-compact.svg">
  <img src="assets/svg/card-paper.svg" width="100%" alt="Research paper: PredictLab, an AI-powered multi-disease clinical risk prediction platform using machine learning and large language model explanations. By Vinayak K V, published 17 May 2026 on Zenodo, DOI 10.5281/zenodo.20253956, CC BY 4.0. Animated figures: a linear SVM boundary for diabetes, a random forest for stroke and a logistic curve for heart disease. Figures are schematic. Llama 3.1 8B explains each result in plain language, as a risk indicator rather than a diagnosis. Read the paper.">
</picture>
</a>

[Read the paper ↗](https://doi.org/10.5281/zenodo.20253956) &nbsp;·&nbsp; [Live demo](https://huggingface.co/spaces/VINAYAKKV/Predict-Ai) &nbsp;·&nbsp; [Code](https://github.com/vinayak533/PredictLab-)

### Portfolio

<p>
<a href="https://www.vinayakkv.com/">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/card-portfolio-compact.svg">
  <img src="assets/svg/card-portfolio.svg" width="100%" alt="Portfolio: vinayakkv.com. I build agents that run real tools and cite their sources. Neo, the site's robot guide, floats, blinks and talks: live traces and receipts for every claim. Open portfolio.">
</picture>
</a>
</p>

### Expertise

<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/expertise-compact.svg">
  <img src="assets/svg/expertise.svg" width="100%" alt="Agent systems (loom.ai): tool execution in a real Linux sandbox, model routing with provider fallback. Grounded generation (loom.ai, lazyhire): answers that cite sources or abstain; CV drafts checked for invented claims. Applied ML (InForge-AI, InsightGenie, NL2SQL): cleaning, EDA and model benchmarking, with local fallbacks when LLMs fail. Product engineering (loom.ai, lazyhire, InForge-AI): WebSocket backends and Next.js products, hardened with CSP, CSRF and E2E tests.">
</picture>

### Technical Skills

<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/stack-compact.svg">
  <img src="assets/svg/stack.svg" width="100%" alt="Languages: Python, TypeScript, SQL, C++. AI &amp; Agents: LangGraph, LangChain, Multi-Agent Systems, RAG, Tool Calling, LLM Routing, Guardrails. ML &amp; Retrieval: PyTorch, Scikit-learn, XGBoost, pgvector, Hybrid Retrieval, MLflow. Backend: FastAPI, WebSockets, Next.js, E2B Sandboxes. Cloud &amp; Data: PostgreSQL, Supabase, SQLite, Docker, AWS, GitHub Actions.">
</picture>

### GitHub activity

<a href="https://github.com/vinayak533?tab=overview">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/activity-compact.svg">
  <img src="assets/svg/activity.svg" width="100%" alt="Weekly GitHub contributions over the last year as a dot matrix, with the last 90 days highlighted. Refreshed daily from GitHub’s contribution calendar by a repository workflow.">
</picture>
</a>

### Contact

<p>
<a href="mailto:vinayakkvjob@gmail.com">
<picture>
  <source media="(max-width: 639px), (min-width: 768px) and (max-width: 959px)" srcset="assets/svg/contact-compact.svg">
  <img src="assets/svg/contact.svg" width="100%" alt="Let’s build AI that shows its work. Open to AI/ML roles. Email vinayakkvjob@gmail.com.">
</picture>
</a>
</p>

[LinkedIn](https://www.linkedin.com/in/vinayak-kv-ds) &nbsp;·&nbsp; [Portfolio](https://www.vinayakkv.com/) &nbsp;·&nbsp; [All repositories](https://github.com/vinayak533?tab=repositories)
