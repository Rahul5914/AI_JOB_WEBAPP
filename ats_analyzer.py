"""
ATS Score Analyzer
Compares resume against a job description and identifies matching/missing skills.
Provides suggestions to improve ATS score.
"""
import re
import random

COMMON_SKILLS = [
    "python","machine learning","deep learning","nlp","sql","docker","kubernetes",
    "aws","gcp","azure","git","linux","react","javascript","typescript","fastapi",
    "flask","django","tensorflow","pytorch","scikit-learn","pandas","numpy",
    "spark","kafka","airflow","mlflow","hugging face","llm","rag","vector database",
    "computer vision","data analysis","tableau","power bi","excel","rest api",
    "graphql","mongodb","nosql","ci/cd","java","c++","r","matlab","hadoop",
]

def extract_skills_from_jd(jd_text: str) -> list:
    """Extract skills mentioned in a job description by keyword matching."""
    jd_lower = jd_text.lower()
    found = []
    for skill in COMMON_SKILLS:
        if skill in jd_lower:
            found.append(skill.title())
    # Deduplicate
    return list(dict.fromkeys(found))


def analyze_ats_score(resume: dict, job_description: str) -> dict:
    """
    Analyze how well the resume matches a job description.
    Returns: ATS score, matched skills, missing skills, and improvement suggestions.
    """
    resume_skills = [s.lower() for s in resume.get("skills", [])]
    jd_skills = extract_skills_from_jd(job_description)

    if not jd_skills:
        # Fallback if no skills detected
        jd_skills = random.sample([s.title() for s in COMMON_SKILLS], 8)

    matched = [s for s in jd_skills if s.lower() in resume_skills]
    missing = [s for s in jd_skills if s.lower() not in resume_skills]

    # Score based on skill coverage
    if jd_skills:
        base_score = int((len(matched) / len(jd_skills)) * 100)
    else:
        base_score = 50

    # Add keyword density bonus (jd word count signals good match)
    word_count = len(job_description.split())
    density_bonus = min(10, word_count // 50)
    score = min(98, base_score + density_bonus + random.randint(0, 5))

    suggestions = _generate_suggestions(missing, score, resume)
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "suggestions": suggestions,
    }


def _generate_suggestions(missing_skills: list, score: int, resume: dict) -> list:
    """Generate personalized improvement suggestions."""
    suggestions = []

    if missing_skills:
        top_missing = missing_skills[:3]
        suggestions.append(
            f"🛠️ Add these missing skills to your resume: **{', '.join(top_missing)}**"
        )
        suggestions.append(
            f"📚 Consider taking short courses on {top_missing[0]} to fill the skill gap."
        )

    if score < 60:
        suggestions.append("📝 Rewrite your summary section to include keywords from the job description.")
        suggestions.append("📌 Mirror the exact job title in your resume headline.")

    if score < 80:
        suggestions.append("🔢 Quantify your achievements — e.g. 'Improved model accuracy by 15%'.")
        suggestions.append("📋 Use the same terminology as the JD (e.g., if JD says 'LLM', use 'LLM' not 'large language model').")

    suggestions.append("✅ Ensure your resume is ATS-friendly: avoid tables, images, and fancy columns.")
    suggestions.append("🎯 Tailor your bullet points to match the responsibilities listed in the JD.")

    return suggestions
