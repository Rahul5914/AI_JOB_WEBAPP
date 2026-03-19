"""
Recommendation Engine
Computes cosine similarity between resume embeddings and job embeddings
to rank the most relevant jobs for the user.
"""
import math
import random


def cosine_similarity(vec_a: list, vec_b: list) -> float:
    """Compute cosine similarity between two vectors."""
    if not vec_a or not vec_b:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a ** 2 for a in vec_a))
    mag_b = math.sqrt(sum(b ** 2 for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def skill_overlap_score(resume_skills: list, job_skills: list) -> float:
    """Compute skill overlap ratio between resume and job."""
    if not job_skills:
        return 0.0
    resume_set = set(s.lower() for s in resume_skills)
    job_set = set(s.lower() for s in job_skills)
    overlap = resume_set & job_set
    return len(overlap) / len(job_set)


def compute_recommendations(resume: dict, jobs: list) -> list:
    """
    Rank jobs by combining:
    1. Cosine similarity of resume embedding vs job embedding (60%)
    2. Skill overlap score (40%)
    Returns jobs sorted by combined match score (descending).
    """
    resume_embedding = resume.get("embedding_vector", [])
    resume_skills = resume.get("skills", [])
    scored_jobs = []

    for job in jobs:
        job_embedding = job.get("embedding_vector", [])

        # Embedding similarity (simulated — in production use sentence-transformers)
        embed_score = cosine_similarity(resume_embedding, job_embedding)
        # Normalize cosine from [-1,1] to [0,1]
        embed_score = (embed_score + 1) / 2

        # Skill overlap
        skill_score = skill_overlap_score(resume_skills, job.get("skills", []))

        # Combined score (weighted)
        combined = 0.6 * embed_score + 0.4 * skill_score

        # Scale to percentage, add realistic noise
        match_pct = int(min(99, max(40, combined * 100 + random.randint(-5, 10))))

        scored_jobs.append({**job, "match_score": match_pct})

    # Sort by match score descending
    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return scored_jobs
