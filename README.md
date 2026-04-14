<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 280" width="860" height="280">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
      .bg { fill: #0d1117; }
      .border { fill: none; stroke: #00F7FF; stroke-width: 1.5; opacity: 0.85; }
      .border-glow { fill: none; stroke: #00F7FF; stroke-width: 3; opacity: 0.15; filter: blur(4px); }
      .ascii { font-family: 'Share Tech Mono', monospace; font-size: 13px; fill: #00F7FF; }
      .sub { font-family: 'Share Tech Mono', monospace; font-size: 13px; fill: #a78bfa; letter-spacing: 3px; }
      .cursor { fill: #00F7FF; }
    </style>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow">
      <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="860" height="280" class="bg" rx="12"/>

  <!-- Outer glow border -->
  <rect x="6" y="6" width="848" height="268" class="border-glow" rx="10"/>
  <!-- Main border -->
  <rect x="10" y="10" width="840" height="260" class="border" rx="8" filter="url(#glow)"/>

  <!-- Corner decorations -->
  <text x="18" y="30" font-family="monospace" font-size="12" fill="#00F7FF" opacity="0.6">╔</text>
  <text x="828" y="30" font-family="monospace" font-size="12" fill="#00F7FF" opacity="0.6">╗</text>
  <text x="18" y="268" font-family="monospace" font-size="12" fill="#00F7FF" opacity="0.6">╚</text>
  <text x="828" y="268" font-family="monospace" font-size="12" fill="#00F7FF" opacity="0.6">╝</text>

  <!-- ASCII Art Name - centered, with glow -->
  <g filter="url(#glow)" opacity="0">
    <animateTransform attributeName="transform" type="translate" values="0,10;0,0" dur="0.6s" fill="freeze" begin="0.2s"/>
    <animate attributeName="opacity" values="0;1" dur="0.6s" fill="freeze" begin="0.2s"/>

    <text x="430" y="68" class="ascii" text-anchor="middle" font-size="12.5">██╗   ██╗██╗███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗  ██╗</text>
    <text x="430" y="84" class="ascii" text-anchor="middle" font-size="12.5">██║   ██║██║████╗  ██║██╔══██╗╚██╗ ██╔╝██╔══██╗██║ ██╔╝</text>
    <text x="430" y="100" class="ascii" text-anchor="middle" font-size="12.5">██║   ██║██║██╔██╗ ██║███████║ ╚████╔╝ ███████║█████╔╝ </text>
    <text x="430" y="116" class="ascii" text-anchor="middle" font-size="12.5">╚██╗ ██╔╝██║██║╚██╗██║██╔══██║  ╚██╔╝  ██╔══██║██╔═██╗ </text>
    <text x="430" y="132" class="ascii" text-anchor="middle" font-size="12.5"> ╚████╔╝ ██║██║ ╚████║██║  ██║   ██║   ██║  ██║██║  ██╗</text>
    <text x="430" y="148" class="ascii" text-anchor="middle" font-size="12.5">  ╚═══╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝</text>
  </g>

  <!-- Divider line -->
  <line x1="80" y1="162" x2="780" y2="162" stroke="#00F7FF" stroke-width="0.6" opacity="0.4">
    <animate attributeName="opacity" values="0;0.4" dur="0.4s" fill="freeze" begin="0.7s"/>
  </line>

  <!-- Subtitle -->
  <text x="430" y="190" class="sub" text-anchor="middle" filter="url(#softglow)" opacity="0">
    DATA SCIENTIST · ML ENGINEER · GENAI BUILDER
    <animate attributeName="opacity" values="0;1" dur="0.8s" fill="freeze" begin="0.9s"/>
  </text>

  <!-- Blinking cursor -->
  <rect x="416" y="200" width="8" height="2" class="cursor" opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.1s" fill="freeze" begin="1.5s"/>
    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" begin="1.5s"/>
  </rect>

  <!-- Bottom tagline -->
  <text x="430" y="240" font-family="monospace" font-size="11" fill="#a78bfa" text-anchor="middle" opacity="0" letter-spacing="1">
    ⚡  Kerala, India  ·  Top 2% LeetCode  ·  Rank 108 / 6,770  ⚡
    <animate attributeName="opacity" values="0;0.85" dur="1s" fill="freeze" begin="1.2s"/>
  </text>
</svg>

</div>

<br/>

---

## 🧬 Who Am I?

<img align="right" width="320" src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" />

```python
class Vinayak:
    name        = "Vinayak K V"
    role        = ["Data Scientist", "ML Engineer", "GenAI Builder"]
    location    = "Kerala, India 🇮🇳"
    education   = "BCA | Data Science & AI — 91% 🎓"
    focus       = ["LLMs", "AI Agents", "RAG", "MLOps"]
    superpower  = "Raw data → Production AI systems"
    leetcode    = "Top 2% Globally 🏆 (Rank 108 / 6,770)"
    motto       = "Models that can't explain themselves aren't ready."

    def current_mission(self):
        return "Build AI that is explainable, scalable & impactful"
```

<br clear="right"/>

---

## 🎯 What I'm Building

<div align="center">

| 🤖 AI Agents | 🧠 LLM Apps | ⚙️ ML Pipelines | 🚢 MLOps |
|:---:|:---:|:---:|:---:|
| Autonomous workflows | Groq · LLaMA · RAG | End-to-end systems | Docker · CI/CD · MLflow |

</div>

---

## 🛠️ Tech Arsenal

<div align="center">

**⚡ Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=black)

**🧠 ML / AI**

![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-189AB4?style=for-the-badge&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

**🚀 MLOps & Deployment**

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**📊 Data & Viz**

![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

**🤖 Generative AI**

![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-F55036?style=for-the-badge&logoColor=white)
![LLaMA](https://img.shields.io/badge/LLaMA_3-0467DF?style=for-the-badge&logo=meta&logoColor=white)
![RAG](https://img.shields.io/badge/RAG_Pipelines-8A2BE2?style=for-the-badge&logoColor=white)

</div>

---

## 🏆 Hall of Fame

<div align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=vinayak533&theme=radical&no-frame=true&column=7&margin-w=8" />
</div>

<br/>

<div align="center">

```
┌─────────────────────────────────────────────────────────┐
│                   🏅  ACHIEVEMENTS                      │
├──────────────────────────────┬──────────────────────────┤
│  🥇 LeetCode Top 2% Globally │  Rank 108 / 6,770        │
│  🐍 HackerRank Python Gold   │  Score: 415              │
│  📊 Kaggle Python Coder      │  Badge Earned            │
│  💡 GeeksforGeeks            │  150+ Problems | 266 pts │
└──────────────────────────────┴──────────────────────────┘
```

</div>

---

## 🐍 Contribution Snake

<p align="center">
  <img src="https://github.com/Platane/snk/raw/output/github-contribution-grid-snake-dark.svg" />
</p>

---

## 🌐 Find Me Here

<div align="center">

[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:vinayakkvjob@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vinayak-kv-ds)
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vinayak533.github.io/VINAYAK_PORTFOLIO/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vinayak533)

</div>

---

<div align="center">

```
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║   "The goal is to turn data into information,         ║
║    and information into insight."                     ║
║                                                       ║
║                          — Carly Fiorina             ║
╚═══════════════════════════════════════════════════════╝
```

<img src="https://komarev.com/ghpvc/?username=vinayak533&color=00F7FF&style=for-the-badge&label=PROFILE+VIEWS" />

*⭐ If my work inspires you — a star means the world! 🚀*

</div>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:1a1a2e&height=130&section=footer&animation=twinkling" />
</p>
