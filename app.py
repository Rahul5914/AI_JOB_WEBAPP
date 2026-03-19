import streamlit as st
import time
import random
from modules.resume_parser import parse_resume
from modules.job_scraper import get_sample_jobs
from modules.recommender import compute_recommendations
from modules.ats_analyzer import analyze_ats_score
from modules.career_assistant import get_career_advice

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Finder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f0c29, #302b63, #24243e);
    color: white;
}
section[data-testid="stSidebar"] * { color: white !important; }

/* Cards */
.job-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    border-left: 5px solid #6C63FF;
    box-shadow: 0 4px 20px rgba(108,99,255,0.1);
    transition: transform 0.2s;
}
.job-card:hover { transform: translateY(-2px); }

.match-badge {
    background: linear-gradient(90deg, #6C63FF, #48c774);
    color: white;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

.skill-tag {
    display: inline-block;
    background: #f0eeff;
    color: #6C63FF;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 13px;
    margin: 3px;
    font-weight: 500;
}

.missing-skill-tag {
    display: inline-block;
    background: #fff0f0;
    color: #e63946;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 13px;
    margin: 3px;
    font-weight: 500;
}

.ats-score-box {
    background: linear-gradient(135deg, #6C63FF, #48c774);
    color: white;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    font-size: 48px;
    font-weight: 700;
}

.metric-card {
    background: linear-gradient(135deg, #6C63FF11, #48c77411);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    border: 1px solid #6C63FF22;
}

/* Hero */
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6C63FF, #48c774);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.hero-sub {
    color: #555;
    font-size: 1.1rem;
    margin-top: 8px;
}

div[data-testid="stButton"] button {
    background: linear-gradient(90deg, #6C63FF, #48c774);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 24px;
}
div[data-testid="stButton"] button:hover { opacity: 0.9; }

.chat-msg-user {
    background: linear-gradient(90deg, #6C63FF, #302b63);
    color: white;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 18px;
    margin: 6px 0;
    max-width: 80%;
    margin-left: auto;
}
.chat-msg-ai {
    background: #f4f4f8;
    color: #222;
    border-radius: 14px 14px 14px 4px;
    padding: 12px 18px;
    margin: 6px 0;
    max-width: 80%;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────
if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = None
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 AI Job Finder")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📄 Resume Upload", "🎯 Job Recommendations",
         "📊 ATS Analyzer", "🤖 Career Assistant", "📈 Dashboard"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    if st.session_state.parsed_resume:
        r = st.session_state.parsed_resume
        st.markdown(f"**👤 {r.get('name','User')}**")
        st.markdown(f"📧 {r.get('email','—')}")
        st.markdown(f"🛠️ {len(r.get('skills',[]))} skills detected")
        st.markdown(f"💼 {r.get('experience_years', 0)} yrs experience")
    else:
        st.info("Upload your resume to get started!")

# ── Pages ─────────────────────────────────────────────────────

# HOME
if page == "🏠 Home":
    st.markdown('<div class="hero-title">Find Your Dream Job<br>with AI ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Upload your resume → Get matched jobs → Auto-apply with one click</div>', unsafe_allow_html=True)
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, label, val in zip(
        [c1, c2, c3, c4],
        ["🎯","📄","🏢","✅"],
        ["Match Accuracy","Resumes Parsed","Jobs Scraped","Applications Sent"],
        ["94%","12K+","85K+","3.2K"]
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:2rem">{icon}</div>
                <div style="font-size:1.6rem;font-weight:700;color:#6C63FF">{val}</div>
                <div style="color:#666;font-size:0.85rem">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### How It Works")
    steps = [
        ("1️⃣","Upload Resume","Our NLP engine parses your skills, experience & education automatically."),
        ("2️⃣","AI Matching","Cosine similarity ranks the best-fit jobs from 85K+ listings."),
        ("3️⃣","ATS Analysis","See your ATS score & get suggestions to beat applicant filters."),
        ("4️⃣","Auto Apply","Browser automation fills & submits applications instantly."),
    ]
    cols = st.columns(4)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:left">
                <div style="font-size:1.6rem">{num}</div>
                <b>{title}</b>
                <p style="color:#666;font-size:0.85rem;margin-top:6px">{desc}</p>
            </div>""", unsafe_allow_html=True)

# RESUME UPLOAD
elif page == "📄 Resume Upload":
    st.markdown("## 📄 Resume Upload & Parsing")
    st.markdown("Upload your resume and let our NLP engine extract all key details.")

    uploaded = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf","docx","txt"])

    col1, col2 = st.columns([1,1])
    with col1:
        if uploaded:
            with st.spinner("🔍 Parsing resume with NLP..."):
                time.sleep(1.5)
                result = parse_resume(uploaded)
                st.session_state.parsed_resume = result
            st.success("✅ Resume parsed successfully!")

            r = result
            st.markdown("### 👤 Extracted Profile")
            st.markdown(f"**Name:** {r.get('name','—')}  |  **Email:** {r.get('email','—')}  |  **Phone:** {r.get('phone','—')}")
            st.markdown(f"**Experience:** {r.get('experience_years',0)} years  |  **Education:** {r.get('education','—')}")

            st.markdown("### 🛠️ Detected Skills")
            skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in r.get("skills",[])])
            st.markdown(skills_html, unsafe_allow_html=True)

            st.markdown("### 💼 Work Experience")
            for exp in r.get("experience",[]):
                st.markdown(f"- **{exp['role']}** at *{exp['company']}* ({exp['duration']})")
        else:
            st.info("👆 Upload your resume above to begin.")

    with col2:
        st.markdown("### 📋 Tips for Better Parsing")
        tips = [
            "Use a single-column layout for best results",
            "Include a dedicated Skills section",
            "Spell out abbreviations (e.g., Machine Learning, not ML)",
            "Use standard section headings (Education, Experience, Skills)",
            "Save as PDF for most accurate parsing",
        ]
        for t in tips:
            st.markdown(f"✅ {t}")

# JOB RECOMMENDATIONS
elif page == "🎯 Job Recommendations":
    st.markdown("## 🎯 AI-Powered Job Recommendations")

    if not st.session_state.parsed_resume:
        st.warning("⚠️ Please upload your resume first.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            location = st.selectbox("📍 Location", ["Remote","Bangalore","Mumbai","Delhi","Hyderabad","Pune","Any"])
        with col2:
            job_type = st.selectbox("💼 Job Type", ["Full-time","Part-time","Contract","Internship"])
        with col3:
            experience = st.selectbox("🏆 Experience", ["0-1 yrs","1-3 yrs","3-5 yrs","5+ yrs"])

        if st.button("🔍 Find Matching Jobs"):
            with st.spinner("🤖 Scraping & matching jobs with AI..."):
                time.sleep(2)
                jobs = get_sample_jobs()
                recs = compute_recommendations(st.session_state.parsed_resume, jobs)
                st.session_state.jobs = jobs
                st.session_state.recommendations = recs
            st.success(f"✅ Found {len(recs)} matching jobs!")

        if st.session_state.recommendations:
            st.markdown(f"### 📋 Top Matches for You")
            for i, job in enumerate(st.session_state.recommendations):
                score = job.get("match_score", 0)
                score_color = "#48c774" if score >= 80 else "#ffdd57" if score >= 60 else "#ff6b6b"
                skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in job.get("skills",[])])
                st.markdown(f"""
                <div class="job-card">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <h4 style="margin:0;color:#222">{job['title']}</h4>
                            <span style="color:#666">🏢 {job['company']} &nbsp;|&nbsp; 📍 {job['location']} &nbsp;|&nbsp; 💰 {job['salary']}</span>
                        </div>
                        <div style="background:{score_color};color:white;padding:8px 18px;border-radius:20px;font-weight:700;font-size:1.1rem">
                            {score}% match
                        </div>
                    </div>
                    <p style="color:#555;margin:10px 0 6px">{job['description']}</p>
                    {skills_html}
                </div>""", unsafe_allow_html=True)

                bc1, bc2, bc3 = st.columns([1,1,4])
                with bc1:
                    if st.button(f"⚡ Auto Apply", key=f"apply_{i}"):
                        with st.spinner("🤖 Submitting application..."):
                            time.sleep(1.5)
                        st.success("✅ Applied!")
                        st.session_state.feedback[job['title']] = "applied"
                with bc2:
                    if st.button(f"💾 Save", key=f"save_{i}"):
                        st.info("Saved!")

# ATS ANALYZER
elif page == "📊 ATS Analyzer":
    st.markdown("## 📊 ATS Score Analyzer")
    st.markdown("Paste a job description to see how well your resume matches and what to improve.")

    if not st.session_state.parsed_resume:
        st.warning("⚠️ Please upload your resume first.")
    else:
        jd = st.text_area("📋 Paste Job Description Here", height=200,
                          placeholder="Paste the full job description here...")

        if st.button("🔍 Analyze ATS Score") and jd:
            with st.spinner("Analyzing..."):
                time.sleep(1.5)
                result = analyze_ats_score(st.session_state.parsed_resume, jd)

            score = result["score"]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="ats-score-box">{score}%<br><span style="font-size:1rem;font-weight:400">ATS Score</span></div>', unsafe_allow_html=True)
            with col2:
                st.metric("✅ Matched Skills", len(result["matched"]))
                matched_html = "".join([f'<span class="skill-tag">{s}</span>' for s in result["matched"]])
                st.markdown(matched_html, unsafe_allow_html=True)
            with col3:
                st.metric("❌ Missing Skills", len(result["missing"]))
                missing_html = "".join([f'<span class="missing-skill-tag">{s}</span>' for s in result["missing"]])
                st.markdown(missing_html, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 💡 AI Improvement Suggestions")
            for s in result["suggestions"]:
                st.markdown(f"- {s}")

# CAREER ASSISTANT
elif page == "🤖 Career Assistant":
    st.markdown("## 🤖 RAG-Based Career Assistant")
    st.markdown("Ask anything about jobs, interviews, career growth, or salary negotiation.")

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            role_class = "chat-msg-user" if msg["role"] == "user" else "chat-msg-ai"
            icon = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(f'<div class="{role_class}">{icon} {msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.text_input("💬 Ask your career question...", key="chat_input",
                                placeholder="e.g. How do I prepare for a Python interview?")
    if st.button("Send 📨") and user_input:
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.spinner("🤖 Thinking..."):
            response = get_career_advice(user_input, st.session_state.parsed_resume)
        st.session_state.chat_history.append({"role":"ai","content":response})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("### 💡 Quick Questions")
    quick = ["How to negotiate salary?","Top skills for Data Science 2025","Prepare for system design interview","How to write a cold email to recruiter"]
    qcols = st.columns(2)
    for i, q in enumerate(quick):
        with qcols[i % 2]:
            if st.button(q, key=f"quick_{i}"):
                st.session_state.chat_history.append({"role":"user","content":q})
                response = get_career_advice(q, st.session_state.parsed_resume)
                st.session_state.chat_history.append({"role":"ai","content":response})
                st.rerun()

# DASHBOARD
elif page == "📈 Dashboard":
    st.markdown("## 📈 Application Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    metrics = [("🎯","Jobs Matched","47"),("📨","Applications Sent","12"),("👀","Profile Views","89"),("📞","Interviews","3")]
    for col, (icon, label, val) in zip([col1,col2,col3,col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:2rem">{icon}</div>
                <div style="font-size:2rem;font-weight:700;color:#6C63FF">{val}</div>
                <div style="color:#666;font-size:0.85rem">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Application Tracker")
    applications = [
        {"Job":"ML Engineer","Company":"Google","Status":"Interview Scheduled","Date":"2025-07-10"},
        {"Job":"Data Scientist","Company":"Microsoft","Status":"Applied","Date":"2025-07-09"},
        {"Job":"AI Engineer","Company":"Amazon","Status":"Rejected","Date":"2025-07-08"},
        {"Job":"NLP Engineer","Company":"Meta","Status":"Applied","Date":"2025-07-07"},
    ]
    status_colors = {"Interview Scheduled":"#48c774","Applied":"#3273dc","Rejected":"#e63946"}
    for app in applications:
        color = status_colors.get(app["Status"], "#888")
        st.markdown(f"""
        <div class="job-card" style="border-left-color:{color}">
            <b>{app['Job']}</b> at {app['Company']}
            &nbsp;&nbsp;<span style="background:{color};color:white;padding:3px 12px;border-radius:20px;font-size:12px">{app['Status']}</span>
            <span style="float:right;color:#888">{app['Date']}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 📊 ML Feedback Loop")
    st.info("🧠 The system learns from your interactions (clicks, saves, applies) to improve future recommendations. Your personalized model updates daily.")
    col1, col2 = st.columns(2)
    with col1:
        st.progress(0.74, text="Recommendation accuracy improving: 74%")
    with col2:
        st.progress(0.91, text="Profile completeness: 91%")
