<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=2563EB&center=true&vCenter=true&width=600&lines=Google+Cloud+Architect+Assistant;Powered+by+Gemini+2.5+Flash;Ask+it+anything+cloud-related;(Please+don't+ask+for+pizza+recipes)" alt="Typing SVG" />

<br/>

![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_2.5_Flash-8E44AD?style=for-the-badge&logo=googlecloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deployed-34A853?style=for-the-badge&logo=googlecloud&logoColor=white)

</div>

---

## What is this?

A Flask app with one job: turn Gemini 2.5 Flash into a no-nonsense Google Cloud Solutions Architect that lives in your browser. Ask it about IAM, Cloud Run, VPCs, whatever — it'll give you real, production-ready guidance. Ask it something *unrelated*, and it'll politely (but firmly) redirect you back to cloud topics. It has boundaries. Respect them.

<!-- 🎬 Drop your own pick here — grab any gif link from https://giphy.com and paste it in:
<div align="center"><img src="PASTE_YOUR_GIF_URL_HERE" width="400"/></div>
-->

## Architecture

```mermaid
flowchart TD
    A["🌐 Client Browser"] -->|"hey, secure my Cloud Run service pls"| B["🐍 Flask + Gunicorn (Cloud Run)"]
    B -->|"hands off the question"| C["✨ Vertex AI — Gemini 2.5 Flash"]
    C -->|"sends back real architecture advice"| A

    style A fill:#e8f0fe,stroke:#4285f4,stroke-width:1.5px
    style B fill:#f3e8ff,stroke:#a855f7,stroke-width:1.5px
    style C fill:#fff4e5,stroke:#f59e0b,stroke-width:1.5px
```

**In plain English:** you ask a question → Flask catches it → Gemini thinks about it like a Cloud Architect → the answer flows right back to your browser. No middlemen, no nonsense.

## See it in action

### ✅ Ask it something real, get something useful
![Good question example](screenshots/good-question.png)

### 🍕 Try to derail it, watch it stay professional
![Off-topic question example](screenshots/pizza-question.png)

### 🛠️ Behind the scenes — built live in Cloud Shell
![Cloud Shell development](screenshots/cloud-shell-dev.png)

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Flask, Gunicorn |
| AI | Gemini 2.5 Flash via Vertex AI (`google-genai` SDK) |
| Frontend | HTML, CSS, vanilla JS — no framework bloat |
| Deployment | Docker → Artifact Registry → Cloud Run |
| Testing | pytest |

## Configuration

<pre>
Runtime SA : gemini-app-runner@&lt;PROJECT_ID&gt;.iam.gserviceaccount.com
Role       : roles/aiplatform.user
Model      : gemini-2.5-flash
Region     : europe-west1
</pre>


## Run it yourself

```bash
pip install -r requirements.txt
export GOOGLE_CLOUD_PROJECT=<your-project-id>
export GOOGLE_CLOUD_LOCATION=europe-west1
python3 app.py
```

Then hit `http://localhost:8080` and start interrogating it about cloud architecture.

## Run the tests

```bash
python3 -m pytest tests/test_app.py -v
```

All green, every time. 🟢

---

<div align="center">


</div>
