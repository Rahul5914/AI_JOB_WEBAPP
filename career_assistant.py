"""
RAG-Based Career Assistant
Retrieves career advice from a knowledge base and generates personalized responses.
In production: use a vector database (Pinecone/Chroma) + LLM (OpenAI/Anthropic).
"""

KNOWLEDGE_BASE = {
    "salary": {
        "keywords": ["salary","negotiate","pay","compensation","offer","package","ctc","lpa"],
        "advice": [
            "💰 **Salary Negotiation Tips:**\n\n"
            "1. **Research first** — Use Glassdoor, AmbitionBox, and LinkedIn Salary to know market rates.\n"
            "2. **Never give the first number** — Let them make the initial offer.\n"
            "3. **Anchor high** — Ask for 20-30% above your target.\n"
            "4. **Negotiate the full package** — Consider equity, bonuses, remote work, and learning budgets.\n"
            "5. **Practice your script:** *'Based on my research and experience, I'm targeting ₹X. Is there flexibility?'*\n"
            "6. **Silence is powerful** — After stating your number, stay quiet and let them respond."
        ],
    },
    "interview": {
        "keywords": ["interview","prepare","question","dsa","system design","behavioral","hr","technical"],
        "advice": [
            "🎯 **Interview Preparation Guide:**\n\n"
            "**Technical Round:**\n"
            "- Practice 50+ LeetCode problems (focus on Arrays, Trees, DP, Graphs)\n"
            "- Review time/space complexity for every solution\n"
            "- For ML roles: know bias-variance tradeoff, regularization, evaluation metrics\n\n"
            "**System Design:**\n"
            "- Study: URL shortener, WhatsApp, Netflix, Twitter design\n"
            "- Know CAP theorem, load balancing, caching, database sharding\n\n"
            "**Behavioral (STAR method):**\n"
            "- Situation → Task → Action → Result\n"
            "- Prepare 5-6 stories about leadership, conflict, failure, success\n\n"
            "**Final 48 hours:** Research the company deeply, prepare 3 thoughtful questions to ask."
        ],
    },
    "resume": {
        "keywords": ["resume","cv","write","improve","format","ats","keyword","profile"],
        "advice": [
            "📄 **Resume Writing Best Practices:**\n\n"
            "1. **One page** for <5 years experience; two pages for senior roles.\n"
            "2. **Start bullets with action verbs:** Built, Designed, Improved, Led, Reduced.\n"
            "3. **Quantify everything:** 'Reduced model latency by 40%' beats 'Improved performance'.\n"
            "4. **ATS-friendly format:** Single column, no tables/images, standard fonts.\n"
            "5. **Tailor for each role:** Adjust the skills section to match the JD keywords.\n"
            "6. **Strong summary:** 3 lines that pack your title, top skills, and biggest win.\n"
            "7. **Use tools:** Enhancv, Zety, or Overleaf for clean, professional layouts."
        ],
    },
    "python": {
        "keywords": ["python","coding","programming","script","pandas","numpy","django","flask"],
        "advice": [
            "🐍 **Python Interview Preparation:**\n\n"
            "**Core Concepts to Master:**\n"
            "- List comprehensions, generators, decorators, context managers\n"
            "- OOP: classes, inheritance, dunder methods\n"
            "- Concurrency: threading vs multiprocessing vs asyncio\n"
            "- Built-ins: map, filter, zip, enumerate, sorted\n\n"
            "**ML/DS Python:**\n"
            "- Pandas: groupby, merge, pivot_table, apply\n"
            "- NumPy: broadcasting, vectorization, array slicing\n"
            "- Sklearn: pipelines, cross-validation, GridSearchCV\n\n"
            "**Common Questions:**\n"
            "- Difference between `deepcopy` and `copy`\n"
            "- How does Python's GIL work?\n"
            "- Explain `*args` and `**kwargs`"
        ],
    },
    "career": {
        "keywords": ["career","growth","path","switch","transition","fresher","experience","job","find","search"],
        "advice": [
            "🚀 **Career Growth Strategy:**\n\n"
            "**For Freshers (0-1 years):**\n"
            "- Build 2-3 strong GitHub projects with READMEs\n"
            "- Target startups and mid-size companies — easier first job\n"
            "- Compete on Kaggle, LeetCode, HackerRank to build credibility\n\n"
            "**For Career Switchers:**\n"
            "- Do a bridge course (e.g., IIT's online ML program, Coursera specialization)\n"
            "- Leverage your domain expertise + new tech skills as a unique angle\n"
            "- Network on LinkedIn — 60% of jobs are filled through referrals\n\n"
            "**General Tips:**\n"
            "- Post your learning journey on LinkedIn weekly\n"
            "- Join communities: Discord servers, local meetups, hackathons\n"
            "- Referrals convert 10x better than cold applications"
        ],
    },
    "default": {
        "keywords": [],
        "advice": [
            "🤖 **AI Career Assistant:**\n\n"
            "I can help you with:\n"
            "- 📝 Resume writing and ATS optimization\n"
            "- 🎯 Interview preparation (technical, DSA, behavioral)\n"
            "- 💰 Salary negotiation strategies\n"
            "- 🚀 Career growth and job search strategies\n"
            "- 🐍 Technical skills guidance (Python, ML, System Design)\n\n"
            "Ask me anything like:\n"
            "*'How do I prepare for a system design interview?'*\n"
            "*'What salary should I negotiate for?'*\n"
            "*'How to switch from software to ML?'*"
        ],
    },
}


def get_career_advice(question: str, resume: dict = None) -> str:
    """
    RAG-based response: retrieves relevant knowledge and generates a response.
    In production: embed question → search vector DB → augment LLM prompt → stream response.
    """
    question_lower = question.lower()
    best_match = "default"
    best_score = 0

    for category, data in KNOWLEDGE_BASE.items():
        if category == "default":
            continue
        score = sum(1 for kw in data["keywords"] if kw in question_lower)
        if score > best_score:
            best_score = score
            best_match = category

    advice = KNOWLEDGE_BASE[best_match]["advice"][0]

    # Personalize if resume is available
    if resume and resume.get("skills"):
        top_skills = resume["skills"][:3]
        advice += f"\n\n---\n💡 *Based on your resume, your top skills are: **{', '.join(top_skills)}**. Highlight these prominently in your applications.*"

    return advice
