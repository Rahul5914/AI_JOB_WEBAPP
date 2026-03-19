# 🚀 AI Job Finder

> An AI-powered platform that automates job discovery, matching, ATS analysis, and career guidance.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## ✨ Features

| Feature | Technology |
|---|---|
| 📄 Resume Parsing | NLP + Regex extraction |
| 🎯 Job Recommendations | Cosine Similarity + Embeddings |
| 📊 ATS Score Analyzer | Keyword matching + Gap analysis |
| 🤖 Career Assistant | RAG-based Q&A system |
| ⚡ Auto Apply Bot | Browser automation (Selenium) |
| 📈 ML Feedback Loop | Interaction-based learning |

---

## 🛠️ Setup & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-job-finder.git
cd ai-job-finder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 🚀 Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → Select your repo → Set `app.py` as the main file
4. Click **Deploy** — done! 🎉

---

## 📁 Project Structure

```
ai-job-finder/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md
└── modules/
    ├── resume_parser.py    # NLP-based resume parsing
    ├── job_scraper.py      # Multi-platform job scraping
    ├── recommender.py      # Cosine similarity recommendation engine
    ├── ats_analyzer.py     # ATS score computation
    └── career_assistant.py # RAG-based career Q&A
```

---

## 🧠 Technical Architecture

```
User → Upload Resume
         ↓
    NLP Parser (skills, experience, education)
         ↓
    Sentence Transformer → Resume Embedding
         ↓
    Cosine Similarity ← Job Embeddings ← Job Scraper (LinkedIn, Indeed, Naukri)
         ↓
    Ranked Job Recommendations
         ↓
    ATS Analyzer → Gap Analysis → Improvement Suggestions
         ↓
    RAG Career Assistant (Vector DB + LLM)
         ↓
    Auto Apply Bot (Selenium Browser Automation)
```

---

## 📜 License

MIT License — free to use, modify, and distribute.
