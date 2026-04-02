#!/bin/bash

# 1. Create the required directory for GitHub Actions
echo "📁 Creating .github/workflows directory..."
mkdir -p .github/workflows

# 2. Generate the README.md file using a heredoc
echo "📝 Writing README.md..."
cat << 'EOF' > README.md
<h1 align="center">👋 Hi, This is Vinayak K V 👋</h1>

<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=2E8B57&center=true&vCenter=true&width=800&height=50&lines=Training+models+like+it's+2050...;Cleaning+data+like+it's+1999...;Turning+data+into+real-world+impact..." alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <img src="https://cdn.dribbble.com/users/1162077/screenshots/3848914/programmer.gif" alt="Developer Desk GIF" width="300" />
</p>

<p align="center">
  <a href="mailto:vinayakkvjob@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://www.linkedin.com/in/vinayak-kv-ds"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://vinayak533.github.io/VINAYAK_PORTFOLIO/"><img src="https://img.shields.io/badge/Portfolio-252525?style=for-the-badge&logo=Google-Chrome&logoColor=white" alt="Portfolio" /></a>
</p>

---

### 🧠 The Mind Behind the Models
Data Scientist and ML Engineer with deep experience designing and scaling end-to-end machine learning pipelines and GenAI applications. Proven track record of delivering data-driven solutions with a focus on operational reliability and high-performance execution.

- 🥇 Currently building **AI Agents, LLM-powered applications, and RAG pipelines**
- 🧠 Making **predictive models and scalable ML systems** to solve real-world problems
- ⚡ Always diving into **new GenAI tech** to stay ahead

---

### 🐍 Contribution Activity
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/vinayak533/vinayak533/output/github-contribution-grid-snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/vinayak533/vinayak533/output/github-contribution-grid-snake.svg">
    <img alt="github contribution grid snake animation" src="https://raw.githubusercontent.com/vinayak533/vinayak533/output/github-contribution-grid-snake.svg">
  </picture>
</p>

---

### 🚀 What I'm Building

* **PredictLab:** An AI-powered disease prediction platform designed to provide accessible health insights.
* **Customer Churn Prediction System:** An end-to-end machine learning pipeline built to analyze user behavior and forecast retention metrics.

---

### 🛠️ Tech Stack

**Languages & Core** <br/>
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white) ![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)

**ML / DL Frameworks** <br/>
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=black) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

**Generative AI & Agents** <br/>
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white) ![HuggingFace](https://img.shields.io/badge/Hugging%20Face-F9AB00?style=for-the-badge&logo=huggingface&logoColor=white) 

**Data & Visualization** <br/>
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)

**Deployment & Tools** <br/>
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=vinayak533&label=Profile%20Views&color=0e75b6&style=flat" alt="Profile Views" />
</p>
EOF

# 3. Generate the GitHub Action YAML file
echo "🐍 Writing .github/workflows/snake.yml..."
cat << 'EOF' > .github/workflows/snake.yml
name: Generate Snake Animation

on:
  schedule:
    - cron: "0 0 * * *" 
  workflow_dispatch:
  push:
    branches:
    - main

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Generate GitHub Contribution Grid Snake
        uses: Platane/snk@v3
        with:
          github_user_name: vinayak533
          outputs: |
            dist/github-contribution-grid-snake.svg
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark

      - name: Push to output branch
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
EOF

echo "✅ Setup complete! Files generated successfully."
echo "🚀 Now run: 'git add .', 'git commit -m \"Added automated profile\"', and 'git push'."
