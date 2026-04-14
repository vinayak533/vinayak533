<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 280" width="860" height="280">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
      .bg { fill: #0d1117; }
      .border { fill: none; stroke: #00F7FF; stroke-width: 1.5; opacity: 0.85; }
      .border-glow { fill: none; stroke: #00F7FF; stroke-width: 3; opacity: 0.15; }
      .ascii { font-family: 'Share Tech Mono', monospace; font-size: 13px; fill: #00F7FF; }
      .sub { font-family: 'Share Tech Mono', monospace; font-size: 13px; fill: #a78bfa; letter-spacing: 2px; }
      .cursor { fill: #00F7FF; }
    </style>

    <filter id="glow">
      <feGaussianBlur stdDeviation="3"/>
    </filter>

    <filter id="softglow">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="860" height="280" class="bg" rx="12"/>

  <!-- Borders -->
  <rect x="6" y="6" width="848" height="268" class="border-glow" rx="10"/>
  <rect x="10" y="10" width="840" height="260" class="border" rx="8"/>

  <!-- Corners -->
  <text x="18" y="30" fill="#00F7FF" opacity="0.6">╔</text>
  <text x="828" y="30" fill="#00F7FF" opacity="0.6">╗</text>
  <text x="18" y="268" fill="#00F7FF" opacity="0.6">╚</text>
  <text x="828" y="268" fill="#00F7FF" opacity="0.6">╝</text>

  <!-- ASCII Name -->
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.2s" fill="freeze"/>

    <text x="430" y="68" class="ascii" text-anchor="middle">██╗   ██╗██╗███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗  ██╗</text>
    <text x="430" y="84" class="ascii" text-anchor="middle">██║   ██║██║████╗  ██║██╔══██╗╚██╗ ██╔╝██╔══██╗██║ ██╔╝</text>
    <text x="430" y="100" class="ascii" text-anchor="middle">██║   ██║██║██╔██╗ ██║███████║ ╚████╔╝ ███████║█████╔╝</text>
    <text x="430" y="116" class="ascii" text-anchor="middle">╚██╗ ██╔╝██║██║╚██╗██║██╔══██║  ╚██╔╝  ██╔══██║██╔═██╗</text>
    <text x="430" y="132" class="ascii" text-anchor="middle"> ╚████╔╝ ██║██║ ╚████║██║  ██║   ██║   ██║  ██║██║  ██╗</text>
    <text x="430" y="148" class="ascii" text-anchor="middle">  ╚═══╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝</text>
  </g>

  <!-- Divider -->
  <line x1="80" y1="162" x2="780" y2="162" stroke="#00F7FF" stroke-width="0.6" opacity="0.4"/>

  <!-- Subtitle -->
  <text x="430" y="190" class="sub" text-anchor="middle" opacity="0">
    DATA SCIENTIST · ML ENGINEER · GENAI BUILDER
    <animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="0.9s" fill="freeze"/>
  </text>

  <!-- Cursor -->
  <rect x="426" y="200" width="8" height="2" class="cursor">
    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
  </rect>

  <!-- Bottom tagline -->
  <text x="430" y="240" font-size="11" fill="#a78bfa" text-anchor="middle" opacity="0">
    ⚡ Kerala, India · Top 2% LeetCode · Rank 108 / 6,770 ⚡
    <animate attributeName="opacity" from="0" to="0.85" dur="1s" begin="1.2s" fill="freeze"/>
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
